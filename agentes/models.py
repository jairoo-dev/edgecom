from django.db import models
from django.contrib.auth.models import User

class Agente(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agente')
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    firma = models.ImageField(upload_to='firmas/')

    def __str__(self):
        return self.nombre