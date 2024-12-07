from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('import/', views.import_products, name='import_products'),
    path('export/', views.export_products, name='export_products'),
    path('update-stock/', views.update_stock, name='update_stock'),
    path('hadoop-analysis/', views.hadoop_analysis, name='hadoop_analysis'),
]

