from django.db import models

class Contacto(models.Model):
    rfc = models.CharField(max_length=13, blank=True, null=True)
    nombre = models.CharField(max_length=200)
    puesto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
