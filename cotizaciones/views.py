from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from decimal import Decimal
import os
from django.conf import settings
from weasyprint import HTML

from .forms import CotizacionForm
from .models import Cotizacion, DetalleCotizacion
from clientes.models import Cliente
from directorio.models import Contacto
from agentes.models import Agente
from productos.models import Producto
from servicios.models import Servicio
from configuracion.models import ConfiguracionEmpresa
from usuarios.decoradores import permiso_requerido

@login_required(login_url='login')
@permiso_requerido('puede_ver_cotizaciones')
def lista_cotizaciones(request):
    agente_filtro = request.GET.get('agente', '')
    status_filtro = request.GET.get('status', '')
    usuario_filtro = request.GET.get('usuario', '')

    if request.user.is_superuser or request.user.is_staff:
        cotizaciones = Cotizacion.objects.all().order_by('-fecha_creacion')
        if agente_filtro:
            cotizaciones = cotizaciones.filter(agente__id=agente_filtro)
        if usuario_filtro == 'sin_usuario':
            cotizaciones = cotizaciones.filter(creado_por__isnull=True)
        elif usuario_filtro:
            cotizaciones = cotizaciones.filter(creado_por__id=usuario_filtro)
    else:
        cotizaciones = Cotizacion.objects.filter(creado_por=request.user).order_by('-fecha_creacion')

    if status_filtro:
        cotizaciones = cotizaciones.filter(status=status_filtro)

    agentes = Agente.objects.all()
    usuarios = User.objects.all().order_by('username') if (request.user.is_superuser or request.user.is_staff) else None
    form = CotizacionForm()
    hoy = timezone.localdate()
    meses_es = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    mes_actual = f"{meses_es[hoy.month]} {hoy.year}"

    # Cálculos dinámicos basados en tu lista de cotizaciones filtered
    total_cotizado = sum(c.total for c in cotizaciones)

    # Filtramos las pendientes (cambia 'PENDIENTE' por cómo lo tengas guardado en tus choices)
    total_pendiente = sum(c.total for c in cotizaciones if c.status == 'PENDIENTE')

    # Total acumulado creado en el mes actual
    total_mes = sum(
        c.total for c in cotizaciones 
        if c.fecha and c.fecha.year == hoy.year and c.fecha.month == hoy.month
    )    
    return render(request, 'cotizaciones/lista_cotizaciones.html', {
        'cotizaciones': cotizaciones,
        'form': form,
        'agentes': agentes,
        'usuarios': usuarios,
        'agente_filtro': agente_filtro,
        'status_filtro': status_filtro,
        'usuario_filtro': usuario_filtro,
        'total_cotizado': total_cotizado,
        'total_pendiente': total_pendiente,
        'total_mes': total_mes,
        'mes_actual': mes_actual,
    })

@login_required(login_url='login')
@permiso_requerido('puede_ver_cotizaciones')
def buscar_cotizaciones(request):
    cotizaciones = []
    rfc = ''
    cliente = None
    total_general = 0
    if request.method == 'POST':
        rfc = request.POST.get('rfc', '')
        if rfc:
            if request.user.is_superuser or request.user.is_staff:
                cotizaciones = Cotizacion.objects.filter(rfc=rfc)
            else:
                cotizaciones = Cotizacion.objects.filter(rfc=rfc, creado_por=request.user)
            total_general = sum(c.total for c in cotizaciones)
            try:
                cliente = Cliente.objects.get(rfc=rfc)
            except Cliente.DoesNotExist:
                cliente = None
    return render(request, 'cotizaciones/buscar_cotizaciones.html', {
        'cotizaciones': cotizaciones,
        'rfc': rfc,
        'cliente': cliente,
        'total_general': total_general,
    })

@login_required(login_url='login')
@permiso_requerido('puede_ver_cotizaciones')
def agregar_cotizacion(request):
    try:
        agente_usuario = request.user.agente
    except:
        agente_usuario = None

    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        if form.is_valid():
            cotizacion = form.save(commit=False)
            total_str = request.POST.get('total_calculado', '0').strip() or '0'
            cotizacion.total = total_str
            cotizacion.creado_por = request.user
            if agente_usuario:
                cotizacion.agente = agente_usuario
            cotizacion.save()
            skus = request.POST.getlist('sku[]')
            claves_sat = request.POST.getlist('clave_sat[]')
            unidades_sat = request.POST.getlist('unidad_sat[]')
            descripciones = request.POST.getlist('descripcion[]')
            cantidades = request.POST.getlist('cantidad[]')
            precios = request.POST.getlist('precio_unitario[]')
            subtotales = request.POST.getlist('subtotal[]')
            for i in range(len(skus)):
                if skus[i] and skus[i].strip():
                    try:
                        cantidad = float(cantidades[i]) if cantidades[i] else 0
                        precio   = float(precios[i]) if precios[i] else 0
                        subtotal = float(subtotales[i]) if subtotales[i] else cantidad * precio
                        if precio == 0:
                            continue  # omitir líneas sin precio
                        DetalleCotizacion.objects.create(
                            cotizacion=cotizacion,
                            sku=skus[i],
                            clave_sat=claves_sat[i],
                            unidad_sat=unidades_sat[i],
                            descripcion=descripciones[i],
                            cantidad=cantidad,
                            precio_unitario=precio,
                            subtotal=subtotal,
                        )
                    except (ValueError, TypeError):
                        continue
            return redirect('lista_cotizaciones')
    else:
        initial = {'agente': agente_usuario} if agente_usuario else {}
        form = CotizacionForm(initial=initial)
        if agente_usuario:
            form.fields['agente'].widget.attrs['disabled'] = True
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    return render(request, 'cotizaciones/agregar_cotizacion.html', {
        'form': form,
        'productos': productos,
        'servicios': servicios,
        'agente_usuario': agente_usuario,
    })

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_cotizacion(request, folio):
    cotizacion = get_object_or_404(Cotizacion, folio=folio)
    if not request.user.is_superuser and not request.user.is_staff:
        if cotizacion.creado_por != request.user:
            return redirect('sin_acceso')
    if request.method == 'POST':
        form = CotizacionForm(request.POST, instance=cotizacion)
        if form.is_valid():
            cotizacion = form.save(commit=False)
            cotizacion.total = request.POST.get('total_calculado', 0)
            cotizacion.save()
            cotizacion.detalles.all().delete()
            skus = request.POST.getlist('sku[]')
            claves_sat = request.POST.getlist('clave_sat[]')
            unidades_sat = request.POST.getlist('unidad_sat[]')
            descripciones = request.POST.getlist('descripcion[]')
            cantidades = request.POST.getlist('cantidad[]')
            precios = request.POST.getlist('precio_unitario[]')
            subtotales = request.POST.getlist('subtotal[]')
            for i in range(len(skus)):
                if skus[i]:
                    DetalleCotizacion.objects.create(
                        cotizacion=cotizacion,
                        sku=skus[i],
                        clave_sat=claves_sat[i],
                        unidad_sat=unidades_sat[i],
                        descripcion=descripciones[i],
                        cantidad=cantidades[i],
                        precio_unitario=precios[i],
                        subtotal=subtotales[i],
                    )
            return redirect('lista_cotizaciones')
    else:
        form = CotizacionForm(instance=cotizacion)
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    detalles = cotizacion.detalles.all()
    return render(request, 'cotizaciones/editar_cotizacion.html', {
        'form': form,
        'cotizacion': cotizacion,
        'detalles': detalles,
        'productos': productos,
        'servicios': servicios,
    })

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_cotizacion(request, folio):
    cotizacion = get_object_or_404(Cotizacion, folio=folio)
    if not request.user.is_superuser and not request.user.is_staff:
        if cotizacion.creado_por != request.user:
            return redirect('sin_acceso')
    if request.method == 'POST':
        cotizacion.delete()
        return redirect('lista_cotizaciones')
    return render(request, 'cotizaciones/eliminar_cotizacion.html', {'cotizacion': cotizacion})

@login_required(login_url='login')
@permiso_requerido('puede_ver_cotizaciones')
def detalle_cotizacion(request, folio):
    cotizacion = get_object_or_404(Cotizacion, folio=folio)
    if not request.user.is_superuser and not request.user.is_staff:
        if cotizacion.creado_por != request.user:
            return redirect('sin_acceso')
    detalles = cotizacion.detalles.all()
    iva_pct = Decimal(cotizacion.iva) / 100 if cotizacion.iva else Decimal('0')
    base = sum(d.subtotal for d in detalles)
    monto_iva = base * iva_pct
    return render(request, 'cotizaciones/detalle_cotizacion.html', {
        'cotizacion': cotizacion,
        'detalles': detalles,
        'base': base,
        'monto_iva': monto_iva,
    })

def api_cliente(request, rfc):
    cliente = get_object_or_404(Cliente, rfc=rfc)
    return JsonResponse({
        'rfc': cliente.rfc,
        'razon_social': cliente.razon_social,
        'codigo_postal': cliente.codigo_postal,
        'regimen_fiscal': cliente.regimen_fiscal,
    })

def api_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    return JsonResponse({
        'nombre': contacto.nombre,
        'puesto': contacto.puesto,
        'telefono': contacto.telefono,
        'email': contacto.email,
        'rfc': contacto.rfc,
    })

def api_agente(request, pk):
    agente = get_object_or_404(Agente, pk=pk)
    return JsonResponse({
        'nombre': agente.nombre,
        'telefono': agente.telefono,
        'email': agente.email,
    })

def api_producto(request, sku):
    producto = get_object_or_404(Producto, sku=sku)
    return JsonResponse({
        'sku': producto.sku,
        'clave_sat': producto.clave_sat,
        'descripcion': producto.descripcion,
        'unidad_sat': producto.unidad_sat,
        'precio_unitario': str(producto.precio_unitario),
    })

@login_required(login_url='login')
@permiso_requerido('puede_ver_cotizaciones')
def generar_pdf(request, folio):
    cotizacion = get_object_or_404(Cotizacion, folio=folio)
    if not request.user.is_superuser and not request.user.is_staff:
        if cotizacion.creado_por != request.user:
            return redirect('sin_acceso')

    detalles = cotizacion.detalles.all()
    iva_pct = Decimal(cotizacion.iva) / 100 if cotizacion.iva else Decimal('0')
    base = sum(d.subtotal for d in detalles)
    monto_iva = base * iva_pct

    empresa = ConfiguracionEmpresa.objects.first()

    # Logo
    if empresa and empresa.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, str(empresa.logo))
    else:
        logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'logo.png')

    # Firma
    firma_path = ''
    if cotizacion.agente and cotizacion.agente.firma:
        firma_path = os.path.join(settings.MEDIA_ROOT, str(cotizacion.agente.firma))

    html_string = render_to_string('cotizaciones/pdf_cotizacion.html', {
        'cotizacion': cotizacion,
        'detalles': detalles,
        'base': base,
        'monto_iva': monto_iva,
        'empresa': empresa,
        'logo_path': f'file:///{logo_path}'.replace('\\', '/'),
        'firma_path': f'file:///{firma_path}'.replace('\\', '/'),
    })

    pdf = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{folio}.pdf"'
    return response
