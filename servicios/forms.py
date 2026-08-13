from django import forms
import html
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['sku', 'clave_sat', 'descripcion', 'unidad_sat', 'precio_unitario']
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control',}),
            'clave_sat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clave SAT'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio'}),
            'unidad_sat': forms.TextInput(attrs={'class': 'form-control',}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '')
        return html.unescape(descripcion)
