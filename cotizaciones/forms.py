from django import forms
from .models import Cotizacion
from core.widgets import ClienteSelect


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['rfc', 'contacto', 'agente', 'cuenta', 'solicitud', 'status', 'iva', 'moneda', 'forma_pago', 'vigencia', 'tiempo_entrega', 'lugar_entrega', 'notas', 'observaciones']
        widgets = {
            'rfc': ClienteSelect(attrs={'class': 'form-select'}),
            'contacto': forms.Select(attrs={'class': 'form-select'}),
            'agente': forms.Select(attrs={'class': 'form-select'}),
            'solicitud': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Texto libre...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'iva': forms.Select(attrs={'class': 'form-select'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'forma_pago': forms.Select(attrs={'class': 'form-select'}),
            'vigencia': forms.Select(attrs={'class': 'form-select'}),
            'tiempo_entrega': forms.Select(attrs={'class': 'form-select'}),
            'lugar_entrega': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar de entrega...'}),
            'cuenta': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas adicionales...'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
