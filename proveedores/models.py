from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    contacto = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.nombre
