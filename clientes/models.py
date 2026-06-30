from django.db import models

class Cliente(models.Model):
    rfc = models.CharField(max_length=13, primary_key=True)
    razon_social = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=5)
    regimen_fiscal = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.rfc


class DocumentoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='documentos')
    archivo = models.FileField(upload_to='documentos_clientes/')
    fecha_subida = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre_archivo()

    def nombre_archivo(self):
        return self.archivo.name.split('/')[-1]
