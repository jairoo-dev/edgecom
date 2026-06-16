from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from agentes.models import Agente

class Factura(models.Model):
    STATUS_CHOICES = [
        ('TIMBRADO', 'Timbrado'),
        ('PAGADO', 'Pagado'),
        ('CREDITO', 'Crédito'),
        ('ADEUDO', 'Adeudo'),
        ('ABONO', 'Abono'),
    ]

    rfc = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='rfc')
    folio = models.CharField(max_length=50, primary_key=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    monto_abono = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_pago = models.DateField(null=True, blank=True, verbose_name='Fecha de Pago / Abono')
    fecha_vencimiento = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    agente = models.ForeignKey(Agente, on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas')
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas')

    def __str__(self):
        return self.folio

    def saldo_pendiente(self):
        if self.status == 'PAGADO':
            return 0
        elif self.status == 'ABONO' and self.monto_abono:
            return self.total - self.monto_abono
        else:
            return self.total
