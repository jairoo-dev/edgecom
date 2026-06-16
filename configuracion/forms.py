from django import forms
from .models import ConfiguracionEmpresa

class ConfiguracionEmpresaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionEmpresa
        fields = ['nombre', 'rfc', 'regimen_fiscal', 'direccion', 'codigo_postal',
                  'telefono', 'whatsapp', 'sitio_web', 'email', 'logo', 
                  'pie_pagina', 'color_primario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'regimen_fiscal': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'sitio_web': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'pie_pagina': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'color_primario': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }