from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def moneda(value):
    """
    Formatea un número como moneda con comas y 2 decimales.
    Ejemplo: 12345.6 → 12,345.60
    Uso en template: {{ factura.total|moneda }}
    """
    try:
        value = Decimal(str(value))
        return f"{value:,.2f}"
    except (InvalidOperation, TypeError, ValueError):
        return value
