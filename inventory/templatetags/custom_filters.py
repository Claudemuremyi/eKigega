from django import template

register = template.Library()

@register.filter
def currency(value):
    try:
        # Format number with thousand separators and add RWF
        formatted = "{:,.0f}".format(float(value))
        return f" {formatted} RWF"
    except (ValueError, TypeError):
        return value