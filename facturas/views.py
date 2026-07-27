from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.utils import timezone
from decimal import Decimal
from weasyprint import HTML
import os
from django.conf import settings
from .forms import FacturaForm, DetalleFacturaFormSet
from .models import Factura, DetalleFactura
from clientes.models import Cliente
from configuracion.models import ConfiguracionEmpresa
from usuarios.decoradores import permiso_requerido
import requests
import base64
from requests.auth import HTTPBasicAuth
from django.contrib import messages
from django.http import JsonResponse
from productos.models import Producto
from servicios.models import Servicio


@login_required(login_url='login')
@permiso_requerido('puede_ver_facturas')
def lista_facturas(request):
    status_filtro = request.GET.get('status', '')
    usuario_filtro = request.GET.get('usuario', '')

    if request.user.is_superuser or request.user.is_staff:
        facturas = Factura.objects.all().order_by('-fecha_creacion')
        if usuario_filtro == 'sin_usuario':
            facturas = facturas.filter(creado_por__isnull=True)
        elif usuario_filtro:
            facturas = facturas.filter(creado_por__id=usuario_filtro)
    else:
        facturas = Factura.objects.filter(creado_por=request.user).order_by('-fecha_creacion')

    if status_filtro:
        facturas = facturas.filter(status=status_filtro)

    hoy = timezone.localdate()
    meses_es = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    mes_actual = f"{meses_es[hoy.month]} {hoy.year}"
    total_facturado  = sum(f.total for f in facturas)
    saldo_pendiente  = sum(f.saldo_pendiente() for f in facturas)
    total_mes        = sum(
        f.total for f in facturas
        if f.fecha_pago and f.fecha_pago.year == hoy.year and f.fecha_pago.month == hoy.month
    )

    usuarios = User.objects.all().order_by('username') if (request.user.is_superuser or request.user.is_staff) else None

    return render(request, 'facturas/lista_facturas.html', {
        'facturas': facturas,
        'status_filtro': status_filtro,
        'usuarios': usuarios,
        'usuario_filtro': usuario_filtro,
        'total_facturado': total_facturado,
        'saldo_pendiente': saldo_pendiente,
        'total_mes': total_mes,
        'mes_actual': mes_actual,
    })

@login_required(login_url='login')
@permiso_requerido('puede_ver_facturas')
def agregar_factura(request):
    try:
        agente_usuario = request.user.agente
    except Exception:
        agente_usuario = None

    if request.method == 'POST':
        form = FacturaForm(request.POST)
        formset = DetalleFacturaFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            factura = form.save(commit=False)
            factura.creado_por = request.user
            
            if agente_usuario:
                factura.agente = agente_usuario
                
            factura.total = Decimal('0.00')
            factura.save()
            
            formset.instance = factura
            partidas = formset.save(commit=False)
            
            total_acumulado = Decimal('0.00')
            for detalle in partidas:
                detalle.save()
                total_acumulado += detalle.total_con_iva()
                
            for obj in formset.deleted_objects:
                obj.delete()
                
            factura.total = round(total_acumulado, 2)
            factura.save()
            
            messages.success(request, f"Factura {factura.folio} guardada con éxito.")
            return redirect('lista_facturas')
    else:
        initial = {'agente': agente_usuario} if agente_usuario else {}
        form = FacturaForm(initial=initial)
        formset = DetalleFacturaFormSet()

    if agente_usuario:
        form.fields['agente'].widget.attrs['disabled'] = True

    productos = Producto.objects.all()
    servicios = Servicio.objects.all()

    return render(request, 'facturas/agregar_factura.html', {
        'form': form,
        'formset': formset,
        'agente_usuario': agente_usuario,
        'productos': productos,  
        'servicios': servicios,  
    })

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_factura(request, folio):
    factura = get_object_or_404(Factura, folio=folio)

    # Bloquear edición si ya está timbrada
    if factura.status == 'TIMBRADO':
        messages.error(request, f"La factura {folio} ya fue timbrada y no puede editarse.")
        return redirect('lista_facturas')
    
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        # Excluimos folio y total de la validación — folio no cambia y total lo calculamos nosotros
        form.fields.pop('folio', None)
        form.fields.pop('total', None)
        if form.is_valid():
            f = form.save(commit=False)
            f.folio = factura.folio  # conservar el folio original
            total_calculado = request.POST.get('total_calculado', '0')
            try:
                f.total = Decimal(total_calculado)
            except Exception:
                f.total = Decimal('0.00')
            f.save()
            
            # Limpiamos los detalles actuales para reemplazar con los nuevos
            factura.detalles.all().delete()
            
            skus = request.POST.getlist('sku[]')
            cantidades = request.POST.getlist('cantidad[]')
            precios = request.POST.getlist('precio_unitario[]')
            
            for i in range(len(skus)):
                if skus[i]:
                    # Buscamos en Producto o en Servicio
                    producto = Producto.objects.filter(sku=skus[i]).first()
                    servicio = Servicio.objects.filter(sku=skus[i]).first()
                    
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=producto, # Será el objeto o None
                        servicio=servicio, # Será el objeto o None
                        cantidad=cantidades[i],
                        precio_unitario=precios[i]
                    )
            return redirect('lista_facturas') # Cambia por tu URL correcta
    else:
        form = FacturaForm(instance=factura)

    return render(request, 'facturas/editar_factura.html', {
        'form': form,
        'factura': factura,
        'detalles': factura.detalles.all(),
        'productos': Producto.objects.all().order_by('descripcion'),
        'servicios': Servicio.objects.all().order_by('descripcion'),
    })

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_factura(request, folio):
    factura = get_object_or_404(Factura, folio=folio)
    if not request.user.is_superuser and not request.user.is_staff:
        if factura.creado_por != request.user:
            return redirect('sin_acceso')
    if request.method == 'POST':
        factura.delete()
        return redirect('lista_facturas')
    return render(request, 'facturas/eliminar_factura.html', {'factura': factura})

@login_required(login_url='login')
@permiso_requerido('puede_ver_facturas')
def buscar_facturas(request):
    facturas = []
    rfc = ''
    saldo_total = 0
    cliente = None
    if request.method == 'POST':
        rfc = request.POST.get('rfc', '')
        if rfc:
            if request.user.is_superuser or request.user.is_staff:
                facturas = Factura.objects.filter(rfc=rfc)
            else:
                facturas = Factura.objects.filter(rfc=rfc, creado_por=request.user)
            saldo_total = sum(f.saldo_pendiente() for f in facturas)
            try:
                cliente = Cliente.objects.get(rfc=rfc)
            except Cliente.DoesNotExist:
                cliente = None
    return render(request, 'facturas/buscar_facturas.html', {
        'facturas': facturas,
        'rfc': rfc,
        'saldo_total': saldo_total,
        'cliente': cliente,
    })

@login_required(login_url='login')
@permiso_requerido('puede_ver_facturas')
def estados_cuenta(request):
    clientes = Cliente.objects.all().order_by('razon_social')
    datos = []
    for cliente in clientes:
        facturas = Factura.objects.filter(rfc=cliente.rfc)
        saldo = sum(f.saldo_pendiente() for f in facturas)
        datos.append({
            'cliente': cliente,
            'total_facturas': facturas.count(),
            'saldo_pendiente': saldo,
        })
    datos.sort(key=lambda x: x['saldo_pendiente'], reverse=True)
    return render(request, 'facturas/estados_cuenta.html', {'datos': datos})

@login_required(login_url='login')
@permiso_requerido('puede_ver_facturas')
def estado_cuenta_pdf(request, rfc):
    cliente = get_object_or_404(Cliente, rfc=rfc)
    facturas = Factura.objects.filter(rfc=rfc)

    saldo_total = sum(f.saldo_pendiente() for f in facturas)
    empresa = ConfiguracionEmpresa.objects.first()

    if empresa and empresa.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, str(empresa.logo))
    else:
        logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'logo.png')

    html_string = render_to_string('facturas/estado_cuenta_pdf.html', {
        'cliente': cliente,
        'facturas': facturas,
        'saldo_total': saldo_total,
        'empresa': empresa,
        'logo_path': f'file:///{logo_path}'.replace('\\', '/'),
    })

    pdf = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="estado_cuenta_{rfc}.pdf"'
    return response

def conectar_facturama(factura):
    """
    Estructura el JSON y realiza la petición a Facturama.
    Lee credenciales y URL desde variables de entorno.
    """
    import os
    url      = os.getenv('FACTURAMA_URL', 'https://apisandbox.facturama.mx/3/cfdis')
    usuario  = os.getenv('FACTURAMA_USER')
    password = os.getenv('FACTURAMA_PASS')

    empresa = ConfiguracionEmpresa.objects.first()
    expedicion = empresa.codigo_postal if empresa and empresa.codigo_postal else '06000'

    items = []
    for item in factura.detalles.all():
        # Usa producto o servicio según cuál esté asignado
        catalogo = item.producto or item.servicio
        if catalogo is None:
            continue

        items.append({
            "Quantity":    float(item.cantidad),
            "ProductCode": catalogo.clave_sat,
            "UnitCode":    catalogo.unidad_sat,
            "Description": catalogo.descripcion,
            "UnitPrice":   float(item.precio_unitario),
            "Subtotal":    float(item.subtotal()),
            "Total":       float(item.total_con_iva()),
            "TaxObject":   item.objeto_impuesto,
            "Taxes": [
                {
                    "Total":      float(item.monto_iva()),
                    "Name":       "IVA",
                    "Rate":       0.16,
                    "IsTransfer": True,
                    "Base":       float(item.subtotal())
                }
            ]
        })

    payload = {
        "Receiver": {
            "Rfc":           factura.rfc.rfc,
            "Name":          factura.rfc.razon_social.upper(),
            "CfdiUse":       factura.uso_cfdi,
            "FiscalRegime":  factura.rfc.regimen_fiscal,
            "TaxZipCode":    factura.rfc.codigo_postal,
        },
        "CfdiType":        "I",
        "PaymentForm":     factura.forma_pago,
        "PaymentMethod":   factura.metodo_pago,
        "ExpeditionPlace": expedicion,
        "Items":           items,
    }

    try:
        auth     = HTTPBasicAuth(usuario, password)
        response = requests.post(url, json=payload, auth=auth)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con Facturama: {e}")
        return None


#@login_required(login_url='login')
@login_required(login_url='login')
@permiso_requerido('puede_ver_facturas')
def timbrar_factura_view(request, folio):
    factura = get_object_or_404(Factura, folio=folio)

    if factura.status == 'TIMBRADO' or factura.uuid:
        messages.warning(request, f"La factura {folio} ya se encuentra timbrada.")
        return redirect('lista_facturas')

    if not factura.detalles.exists():
        messages.error(request, f"La factura {folio} no tiene conceptos. Agrégalos antes de timbrar.")
        return redirect('lista_facturas')

    response = conectar_facturama(factura)

    if response is not None and response.status_code == 201:
        try:
            data = response.json()
            # Guardar UUID del CFDI para futuras cancelaciones y descargas
            factura.uuid   = data.get('Id') or data.get('UUID') or data.get('uuid', '')
            factura.status = 'TIMBRADO'
            factura.save()
            messages.success(request, f"Factura {factura.folio} timbrada exitosamente. UUID: {factura.uuid}")
        except Exception:
            factura.status = 'TIMBRADO'
            factura.save()
            messages.success(request, f"Factura {factura.folio} timbrada exitosamente.")
    else:
        try:
            error_data = response.json()
            motivo = error_data.get('Message', 'La solicitud no es válida.')
            if 'ModelState' in error_data:
                detalles = []
                for campo, errores in error_data['ModelState'].items():
                    campo_limpio = campo.replace('cfdi.', '')
                    err_texto = ", ".join(errores) if isinstance(errores, list) else str(errores)
                    detalles.append(f"[{campo_limpio}: {err_texto}]")
                motivo += " " + " ".join(detalles)
        except Exception:
            status_code = response.status_code if response is not None else "Sin conexión"
            motivo = f"Código HTTP {status_code} — Error al procesar la respuesta."

        messages.error(request, f"No se pudo timbrar {factura.folio}. Motivo: {motivo}")

    return redirect('lista_facturas')

def obtener_precio_producto(request, sku):
    try:
        producto = Producto.objects.get(sku=sku)
        return JsonResponse({'precio': float(producto.precio_unitario)})
    except Producto.DoesNotExist:
        return JsonResponse({'precio': 0}, status=404)
    
def descargar_archivo_sat(id_facturama, formato):
    """
    Descarga el archivo XML o PDF desde el entorno Sandbox de Facturama (API Web).
    Endpoint: GET https://apisandbox.facturama.mx/api/Cfdi/{formato}/issued/{id}
    """
    url = f"https://apisandbox.facturama.mx/api/Cfdi/{formato}/issued/{id_facturama}"
    
    USER_SANDBOX = "EDGEPRUEBAS"
    PASS_SANDBOX = "eFv.7wHWkh4LeEr"
    
    try:
        auth = HTTPBasicAuth(USER_SANDBOX, PASS_SANDBOX)
        response = requests.get(url, auth=auth)
        print(f"[Facturama descarga {formato}] Status: {response.status_code} URL: {url}")
        print(f"[Facturama descarga {formato}] Body: {response.text[:300]}")
        
        if response.status_code == 200:
            data = response.json()
            archivo_base64 = data.get("Content")
            if archivo_base64:
                return base64.b64decode(archivo_base64)
    except Exception as e:
        print(f"Error al descargar archivo {formato} de Sandbox: {e}")
        
    return None
