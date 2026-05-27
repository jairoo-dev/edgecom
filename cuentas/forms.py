from django import forms
from .models import CuentaBancaria

class CuentaBancariaForm(forms.ModelForm):
    class Meta:
        model = CuentaBancaria
        fields = ['banco', 'numero_cuenta', 'clabe', 'beneficiario', 'moneda']
        widgets = {
            'banco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. BBVA'}),
            'numero_cuenta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de cuenta'}),
            'clabe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CLABE interbancaria'}),
            'beneficiario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Beneficiario'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
        }