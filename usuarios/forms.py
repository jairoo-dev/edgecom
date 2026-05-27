from django import forms
from django.contrib.auth.models import User
from .models import Rol, PerfilUsuario

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = [
            'nombre', 'descripcion',
            'puede_ver_facturas', 'puede_ver_cotizaciones',
            'puede_ver_clientes', 'puede_ver_productos', 'puede_ver_servicios',
            'puede_ver_directorio', 'puede_ver_agentes', 'puede_ver_cuentas',
            'puede_editar', 'puede_eliminar',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del rol'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descripción...'}),
            'puede_ver_facturas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_ver_cotizaciones': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_ver_clientes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_ver_productos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_ver_servicios': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_ver_directorio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_ver_agentes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_ver_cuentas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_editar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_eliminar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        required=False,
        label='Contraseña'
    )
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label='Rol'
    )
    activo = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Activo'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        }