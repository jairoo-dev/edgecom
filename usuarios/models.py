from django.db import models
from django.contrib.auth.models import User

class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    # Módulos principales
    puede_ver_facturas = models.BooleanField(default=False)
    puede_ver_cotizaciones = models.BooleanField(default=False)

    # Catálogo
    puede_ver_clientes = models.BooleanField(default=False)
    puede_ver_productos = models.BooleanField(default=False)
    puede_ver_servicios = models.BooleanField(default=False)
    puede_ver_directorio = models.BooleanField(default=False)
    puede_ver_agentes = models.BooleanField(default=False)
    puede_ver_cuentas = models.BooleanField(default=False)

    # Acciones
    puede_editar = models.BooleanField(default=False)
    puede_eliminar = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username