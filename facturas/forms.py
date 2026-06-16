from django import forms
from .models import Factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['folio', 'rfc', 'agente', 'total', 'status', 'monto_abono', 'fecha_pago', 'fecha_vencimiento', 'notas']
        widgets = {
            'folio':            forms.TextInput(attrs={'class': 'form-control'}),
            'rfc':              forms.Select(attrs={'class': 'form-select'}),
            'agente':           forms.Select(attrs={'class': 'form-select'}),
            'total':            forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'status':           forms.Select(attrs={'class': 'form-select'}),
            'monto_abono':      forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'fecha_pago':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notas':            forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas adicionales...'}),
        }
