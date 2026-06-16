from django.db import models

class Contacto(models.Model):
    TIPO_CHOICES = [
        ('CLIENTE', 'Cliente'),
        ('PROVEEDOR', 'Proveedor'),
    ]

    rfc = models.CharField(max_length=13, blank=True, null=True)
    nombre = models.CharField(max_length=200)
    puesto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='CLIENTE')
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
