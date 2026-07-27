from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from agentes.models import Agente
from productos.models import Producto
from servicios.models import Servicio 
from decimal import Decimal

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
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    facturama_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID único en Facturama")
    uuid = models.CharField(max_length=36, blank=True, null=True, help_text="Folio Fiscal otorgado por el SAT")

    forma_pago = models.CharField(max_length=2, default='03', help_text="Ej: 03=Transferencia, 01=Efectivo")
    metodo_pago = models.CharField(max_length=3, default='PUE', help_text="PUE (Una sola exhibición) o PPD (Parcialidades)")
    uso_cfdi = models.CharField(max_length=4, default='G03', help_text="Ej: G03=Gastos en general, DE01=Gastos médicos")

    xml_sat = models.FileField(upload_to='facturas_sat/xml/', blank=True, null=True)
    pdf_sat = models.FileField(upload_to='facturas_sat/pdf/', blank=True, null=True)

    def __str__(self):
        return self.folio

    def saldo_pendiente(self):
        if self.status == 'PAGADO':
            return Decimal('0.00')
        elif self.status == 'ABONO' and self.monto_abono:
            return self.total - self.monto_abono
        else:
            return self.total

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    objeto_impuesto = models.CharField(max_length=2, default='02', help_text="02 = Sí objeto de impuesto")
    
    def __str__(self):
        descripcion = self.producto.descripcion if self.producto else self.servicio.descripcion
        return f"{self.cantidad} x {descripcion} (Folio: {self.factura.folio})"

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def monto_iva(self):
        return self.subtotal() * Decimal('0.16')
    
    def total_con_iva(self):
        return self.subtotal() + self.monto_iva()