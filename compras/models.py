from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from proveedores.models import Proveedor

class Compra(models.Model):
    STATUS_CHOICES = [
        ('RECIBIDA', 'Recibida'),
        ('PAGADA', 'Pagada'),
        ('CREDITO', 'Crédito'),
        ('ADEUDO', 'Adeudo'),
        ('ABONO', 'Abono'),
    ]

    FORMA_PAGO_CHOICES = [
        ('TRANSFERENCIA', 'Transferencia'),
        ('CHEQUE', 'Cheque'),
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA_DEBITO', 'Tarjeta de Débito'),
        ('TARJETA_CREDITO', 'Tarjeta de Crédito')
    ]

    folio = models.CharField(max_length=50, primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RECIBIDA')
    monto_abono = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_pago = models.DateField(null=True, blank=True, verbose_name='Fecha de Pago / Abono')
    forma_pago = models.CharField(max_length=15, choices=FORMA_PAGO_CHOICES, null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.folio

    def saldo_pendiente(self):
        if self.status == 'PAGADA':
            return 0
        elif self.status == 'ABONO' and self.monto_abono:
            return self.total - self.monto_abono
        else:
            return self.total


def generar_folio_orden():
    ultima = OrdenCompra.objects.order_by('-folio_orden').first()
    if ultima:
        try:
            numero = int(ultima.folio_orden.replace('OC', '')) + 1
        except:
            numero = 1
    else:
        numero = 1
    return f'OC{numero:04d}'


class OrdenCompra(models.Model):
    FORMA_PAGO_CHOICES = [
        ('TRANSFERENCIA', 'Transferencia'),
        ('CREDITO', 'Crédito'),
        ('DEBITO', 'Débito'),
        ('EFECTIVO', 'Efectivo'),
    ]

    MONEDA_CHOICES = [
        ('MXN', 'MXN'),
        ('USD', 'USD'),
    ]

    folio_orden = models.CharField(max_length=50, primary_key=True, default=generar_folio_orden, editable=False)
    fecha = models.DateField(default=timezone.localdate)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='ordenes')
    folio_cotizacion = models.CharField(max_length=50, blank=True, null=True)
    usuario_solicita = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_compra')
    forma_pago = models.CharField(max_length=15, choices=FORMA_PAGO_CHOICES, blank=True, null=True)
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default='MXN')
    cotizacion_interna = models.TextField(blank=True, null=True)
    numero_pedido_cliente = models.CharField(max_length=100, blank=True, null=True)
    autorizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_autorizadas')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.folio_orden


class DetalleOrdenCompra(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    sku = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.sku} - {self.orden}'
