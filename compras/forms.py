from django import forms
from .models import Compra, OrdenCompra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['folio', 'proveedor', 'total', 'status', 'monto_abono', 'fecha', 'fecha_vencimiento', 'fecha_pago', 'forma_pago', 'notas']
        widgets = {
            'folio':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Folio de la factura'}),
            'proveedor':        forms.Select(attrs={'class': 'form-select'}),
            'total':            forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'status':           forms.Select(attrs={'class': 'form-select'}),
            'monto_abono':      forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'fecha':            forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_pago':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'forma_pago':       forms.Select(attrs={'class': 'form-select'}),
            'notas':            forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionales...'}),
        }


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'folio_cotizacion', 'forma_pago', 'moneda', 'cotizacion_interna', 'numero_pedido_cliente', 'autorizado_por', 'notas']
        widgets = {
            'proveedor':            forms.Select(attrs={'class': 'form-select'}),
            'folio_cotizacion':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Folio de cotización proveedor'}),
            'forma_pago':           forms.Select(attrs={'class': 'form-select'}),
            'moneda':               forms.Select(attrs={'class': 'form-select'}),
            'cotizacion_interna':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Folio cotización interna'}),
            'numero_pedido_cliente':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de pedido del cliente'}),
            'autorizado_por':       forms.Select(attrs={'class': 'form-select'}),
            'notas':                forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionales...'}),
        }
