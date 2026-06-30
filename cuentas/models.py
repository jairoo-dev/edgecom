from django.db import models

class CuentaBancaria(models.Model):
    MONEDA_CHOICES = [
        ('MXN', 'MXN'),
        ('USD', 'USD'),
    ]

    banco = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=50)
    clabe = models.CharField(max_length=18)
    beneficiario = models.CharField(max_length=200)
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default='MXN')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.banco} - {self.beneficiario}'