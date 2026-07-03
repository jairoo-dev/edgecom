from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from clientes.models import Cliente

def generar_folio():
    ultima = Cotizacion.objects.order_by('-folio').first()
    if ultima:
        try:
            numero = int(ultima.folio.replace('EDGE', '')) + 1
        except:
            numero = 1
    else:
        numero = 1
    return f'EDGE{numero:04d}'

class Cotizacion(models.Model):
    STATUS_CHOICES = [
        ('ENVIADO', 'Enviado'),
        ('NEGOCIACION', 'Negociación'),
        ('PERDIDO', 'Perdido'),
        ('FACTURADO', 'Facturado'),
    ]

    MONEDA_CHOICES = [
        ('MXN', 'MXN'),
        ('USD', 'USD'),
    ]

    FORMA_PAGO_CHOICES = [
        ('ANTICIPADO', 'Por anticipado al recibir orden de compra'),
        ('ANTICIPO_25', 'Se requiere anticipo 25%'),
        ('ANTICIPO_50', 'Se requiere anticipo 50%'),
        ('ANTICIPO_75', 'Se requiere anticipo 75%'),
        ('CONTRA_ENTREGA', 'Contra entrega'),
        ('CONTRA_EMBARQUE', 'Contra aviso de embarque'),
        ('CREDITO_15', 'Crédito 15 días'),
        ('CREDITO_30', 'Crédito 30 días'),
        ('CREDITO_60', 'Crédito 60 días'),
        ('CREDITO_90', 'Crédito 90 días'),
    ]

    VIGENCIA_CHOICES = [
        ('10', '10 días'),
        ('30', '30 días'),
        ('60', '60 días'),
    ]

    ENTREGA_CHOICES = [
        ('3', '3 días'),
        ('5', '5 días'),
        ('7', '7 días'),
        ('10', '10 días'),
        ('2S', '2 semanas'),
        ('4S', '4 semanas'),
        ('6S', '6 semanas'),
        ('8S', '8 semanas'),
        ('12S', '12 semanas'),
    ]

    IVA_CHOICES = [
        ('0', '0%'),
        ('8', '8%'),
        ('16', '16%'),
    ]

    folio = models.CharField(max_length=50, primary_key=True, default=generar_folio, editable=False)
    rfc = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='rfc', null=True, blank=True)
    contacto = models.ForeignKey('directorio.Contacto', on_delete=models.SET_NULL, null=True, blank=True)
    agente = models.ForeignKey('agentes.Agente', on_delete=models.SET_NULL, null=True, blank=True)
    solicitud = models.TextField(blank=True, null=True)
    fecha = models.DateField(default=timezone.localdate)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, blank=True, null=True)
    iva = models.CharField(max_length=2, choices=IVA_CHOICES, default='16', blank=True, null=True)
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default='MXN', blank=True, null=True)
    forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO_CHOICES, blank=True, null=True)
    vigencia = models.CharField(max_length=3, choices=VIGENCIA_CHOICES, blank=True, null=True)
    tiempo_entrega = models.CharField(max_length=3, choices=ENTREGA_CHOICES, blank=True, null=True)
    lugar_entrega = models.TextField(blank=True, null=True)
    cuenta = models.ForeignKey('cuentas.CuentaBancaria', on_delete=models.SET_NULL, null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cotizaciones')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.folio

class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalles')
    sku = models.CharField(max_length=50)
    clave_sat = models.CharField(max_length=50)
    unidad_sat = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.sku} - {self.cotizacion}'
