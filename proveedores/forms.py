from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'rfc', 'contacto', 'telefono', 'email', 'direccion', 'notas']
        widgets = {
            'nombre':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o razón social'}),
            'rfc':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFC'}),
            'contacto':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del contacto'}),
            'telefono':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email':     forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dirección'}),
            'notas':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionales'}),
        }
