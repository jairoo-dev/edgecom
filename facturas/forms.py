from django import forms
from django.forms import inlineformset_factory
from .models import Factura, DetalleFactura  
from core.widgets import ClienteSelect       
from productos.models import Producto
from servicios.models import Servicio

class FacturaForm(forms.ModelForm):
    
    FORMA_PAGO_CHOICES = [
        ('', 'Seleccione o escriba forma de pago...'),
        ('01', '[01] Efectivo'),
        ('02', '[02] Cheque nominativo'),
        ('03', '[03] Transferencia electrónica de fondos'),
        ('04', '[04] Tarjeta de crédito'),
        ('28', '[28] Tarjeta de débito'),
        ('99', '[99] Por definir'),
    ]

    METODO_PAGO_CHOICES = [
        ('', 'Seleccione o escriba método de pago...'),
        ('PUE', '[PUE] Pago en una sola exhibición'),
        ('PPD', '[PPD] Pago en parcialidades o diferido'),
    ]

    USO_CFDI_CHOICES = [
        ('', 'Seleccione o escriba uso de CFDI...'),
        ('G01', '[G01] Adquisición de mercancías'),
        ('G03', '[G03] Gastos en general'),
        ('I01', '[I01] Construcciones'),
        ('I04', '[I04] Equipo de cómputo y accesorios'),
        ('S01', '[S01] Sin efectos fiscales'),
        ('CP01', '[CP01] Pagos'),
    ]
    
    forma_pago = forms.ChoiceField(choices=FORMA_PAGO_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    metodo_pago = forms.ChoiceField(choices=METODO_PAGO_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    uso_cfdi = forms.ChoiceField(choices=USO_CFDI_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Factura
        fields = [
            'folio', 'rfc', 'agente', 'total', 'status', 
            'monto_abono', 'fecha_pago', 'fecha_vencimiento', 'notas',
            'forma_pago', 'metodo_pago', 'uso_cfdi'
        ]
        widgets = {
            'folio':             forms.TextInput(attrs={'class': 'form-control'}),
            'rfc':               ClienteSelect(attrs={'class': 'form-select'}),
            'agente':            forms.Select(attrs={'class': 'form-select'}),
            'total':             forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'readonly': 'readonly'}),
            'status':            forms.Select(attrs={'class': 'form-select'}),
            'monto_abono':       forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'fecha_pago':        forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notas':             forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas adicionales...'}),
            
            'forma_pago':        forms.Select(attrs={'class': 'form-select'}),
            'metodo_pago':       forms.Select(attrs={'class': 'form-select'}),
            'uso_cfdi':          forms.Select(attrs={'class': 'form-select'}),
        }


class DetalleFacturaForm(forms.ModelForm):
    item_sku = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Concepto"
    )

    class Meta:
        model = DetalleFactura
        fields = ['item_sku', 'cantidad', 'precio_unitario']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        productos = Producto.objects.all().order_by('descripcion')
        servicios = Servicio.objects.all().order_by('descripcion')
        
        prod_choices = [(p.sku, f" {p.descripcion} (Prod)") for p in productos]
        serv_choices = [(s.sku, f" {s.descripcion} (Serv)") for s in servicios]
        
        self.fields['item_sku'].choices = [('', 'Seleccione un concepto...')] + prod_choices + serv_choices

        if self.instance and self.instance.pk:
            if self.instance.producto:
                self.fields['item_sku'].initial = self.instance.producto.sku
            elif self.instance.servicio:
                self.fields['item_sku'].initial = self.instance.servicio.sku

    def save(self, commit=True):
        instance = super().save(commit=False)
        sku = self.cleaned_data.get('item_sku')
        
        if sku:
            producto = Producto.objects.filter(sku=sku).first()
            if producto:
                instance.producto = producto
                instance.servicio = None
            else:
                servicio = Servicio.objects.filter(sku=sku).first()
                if servicio:
                    instance.servicio = servicio
                    instance.producto = None
        else:
            instance.producto = None
            instance.servicio = None
            
        if commit:
            instance.save()
        return instance


DetalleFacturaFormSet = inlineformset_factory(
    Factura,
    DetalleFactura,
    form=DetalleFacturaForm, 
    extra=1,             
    can_delete=True
)