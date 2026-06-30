from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'puesto', 'telefono', 'email', 'tipo', 'notas']
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'puesto':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Puesto'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email':    forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'tipo':     forms.Select(attrs={'class': 'form-select'}),
            'notas':    forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionales...'}),
        }
