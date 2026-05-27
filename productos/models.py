from django.db import models

class Producto(models.Model):
    sku = models.CharField(max_length=50, primary_key=True)
    clave_sat = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    unidad_sat = models.CharField(max_length=50)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descripcion