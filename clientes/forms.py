from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rfc', 'razon_social', 'codigo_postal', 'regimen_fiscal']
        widgets = {
            'rfc': forms.TextInput(attrs={'class': 'form-control',}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control',}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control',}),
            'regimen_fiscal': forms.TextInput(attrs={'class': 'form-control',}),
        }
