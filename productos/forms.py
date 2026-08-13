from django import forms
import html
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'clave_sat', 'descripcion', 'unidad_sat', 'precio_unitario']
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control',}),
            'clave_sat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clave SAT'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del producto'}),
            'unidad_sat': forms.TextInput(attrs={'class': 'form-control',}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }

    def clean_descripcion(self):
        # Decodifica entidades HTML (&quot; &amp; etc.) que llegan al copiar texto
        # desde páginas web, para que no se guarden literalmente.
        descripcion = self.cleaned_data.get('descripcion', '')
        return html.unescape(descripcion)
