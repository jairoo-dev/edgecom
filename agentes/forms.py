from django import forms
from django.contrib.auth.models import User
from .models import Agente

class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['nombre', 'telefono', 'email', 'firma', 'user']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'firma': forms.FileInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
        }