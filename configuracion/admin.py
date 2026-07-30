from django.contrib import admin
from .models import ConfiguracionEmpresa


@admin.register(ConfiguracionEmpresa)
class ConfiguracionEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rfc', 'telefono', 'email')
    search_fields = ('nombre', 'rfc')
