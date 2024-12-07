from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import F, Sum
from django.conf import settings
from .models import Product, Sale
from .forms import ProductForm, ExportForm
import csv
import io
import json
import os
import requests
from collections import Counter, defaultdict
from django.contrib import messages
from datetime import datetime

@login_required
def dashboard(request):
    # Get basic metrics
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock_quantity__lte=F('low_stock_threshold'))
    low_stock_count = low_stock_products.count()
    total_sales = 0  # You can implement actual sales calculation here
    
    # Get Hadoop analysis results from session
    hadoop_results = request.session.get('hadoop_results', {})
    
    context = {
        'total_products': total_products,
        'total_sales': total_sales,
        'low_stock_count': low_stock_count,
        'low_stock_products': low_stock_products,
        'hadoop_results': hadoop_results,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'action': 'Create'})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'action': 'Update'})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})

@login_required
def update_stock(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = request.POST.get('new_quantity')
        try:
            product = Product.objects.get(pk=product_id)
            product.stock_quantity = new_quantity
            product.save()
            return JsonResponse({'success': True, 'new_quantity': new_quantity})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def import_products(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        for row in reader:
            try:
                Product.objects.create(
                    name=row['Name'],
                    description=row.get('Description', ''),
                    price=float(row['Price']),
                    stock_quantity=int(row['Stock Quantity']),
                    low_stock_threshold=int(row.get('Low Stock Threshold', 0))
                )
            except (KeyError, ValueError) as e:
                print(f"Skipping row due to error: {e}")
                continue

        return redirect('product_list')
    return render(request, 'inventory/import_products.html')

@login_required
def export_products(request):
    form = ExportForm(request.GET)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        products = Product.objects.all()
        if start_date and end_date:
            products = products.filter(created_at__range=[start_date, end_date])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products_export.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Description', 'Price', 'Stock Quantity', 'Low Stock Threshold', 'Created At'])
        for product in products:
            writer.writerow([product.name, product.description, product.price, product.stock_quantity, product.low_stock_threshold, product.created_at])
        return response
    return render(request, 'inventory/export_products.html', {'form': form})

def analyze_csv(file_content):
    io_string = io.StringIO(file_content)
    reader = csv.DictReader(io_string)
    
    # Identify the correct column names
    sample_row = next(reader, None)
    if not sample_row:
        raise ValueError("The CSV file is empty")
    
    name_column = next((col for col in sample_row.keys() if col.lower().replace(" ", "_") in ['name', 'product_name', 'product']), None)
    quantity_column = next((col for col in sample_row.keys() if col.lower().replace(" ", "_") in ['quantity', 'stock_quantity', 'stock']), None)
    price_column = next((col for col in sample_row.keys() if col.lower().replace(" ", "_") in ['price', 'unit_price', 'cost']), None)

    if not all([name_column, quantity_column, price_column]):
        raise ValueError("Missing required columns in the CSV file")

    # Reset the file pointer
    io_string.seek(0)
    next(reader)  # Skip the header row

    # Perform the analysis
    product_count = Counter()
    total_stock = Counter()
    total_value = Counter()
    for row in reader:
        name = row[name_column]
        try:
            stock = int(row[quantity_column])
            price = float(row[price_column])
        except ValueError:
            continue  # Skip rows with invalid data
        product_count[name] += 1
        total_stock[name] += stock
        total_value[name] += stock * price
    
    analysis_results = {
        'product_count': dict(product_count),
        'total_stock': dict(total_stock),
        'total_value': dict(total_value),
        'average_stock': {name: total_stock[name] / count for name, count in product_count.items() if count > 0},
        'average_value': {name: total_value[name] / count for name, count in product_count.items() if count > 0}
    }
    return analysis_results

@login_required
def hadoop_analysis(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, 'No file uploaded')
            return redirect('hadoop_analysis')

        uploaded_file = request.FILES['file']
        if not uploaded_file.name.endswith('.csv'):
            messages.error(request, 'File is not a CSV')
            return redirect('hadoop_analysis')

        try:
            file_content = uploaded_file.read().decode('utf-8')
            results = analyze_csv(file_content)
            
            request.session['hadoop_results'] = results
            messages.success(request, 'Analysis completed successfully')
            return redirect('dashboard')
            
        except ValueError as e:
            messages.error(request, f'Error in CSV file: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error during analysis: {str(e)}')
        
        return redirect('hadoop_analysis')

    return render(request, 'inventory/hadoop_analysis.html')

