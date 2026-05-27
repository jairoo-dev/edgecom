from django import forms
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
