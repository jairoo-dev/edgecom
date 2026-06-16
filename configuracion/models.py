from django.db import models

class ConfiguracionEmpresa(models.Model):
    nombre = models.CharField(max_length=200)
    rfc = models.CharField(max_length=13)
    regimen_fiscal = models.CharField(max_length=100)
    direccion = models.TextField()
    codigo_postal = models.CharField(max_length=5)
    telefono = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    sitio_web = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='configuracion/', blank=True, null=True)
    pie_pagina = models.TextField(blank=True, null=True)
    color_primario = models.CharField(max_length=7, default='#1a5276')

    class Meta:
        verbose_name = 'Configuración de Empresa'

    def __str__(self):
        return self.nombre