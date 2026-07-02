from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from decimal import Decimal
from weasyprint import HTML
import os
from django.conf import settings
from .forms import FacturaForm
from .models import Factura
from clientes.models import Cliente
from configuracion.models import ConfiguracionEmpresa
from usuarios.decoradores import permiso_requerido

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
        if form.is_valid():
            factura = form.save(commit=False)
            factura.creado_por = request.user
            if agente_usuario:
                factura.agente = agente_usuario
            factura.save()
            return redirect('lista_facturas')
    else:
        initial = {'agente': agente_usuario} if agente_usuario else {}
        form = FacturaForm(initial=initial)

    if agente_usuario:
        form.fields['agente'].widget.attrs['disabled'] = True

    return render(request, 'facturas/agregar_factura.html', {
        'form': form,
        'agente_usuario': agente_usuario,
    })

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_factura(request, folio):
    factura = get_object_or_404(Factura, folio=folio)
    if not request.user.is_superuser and not request.user.is_staff:
        if factura.creado_por != request.user:
            return redirect('sin_acceso')
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            return redirect('lista_facturas')
    else:
        form = FacturaForm(instance=factura)
    return render(request, 'facturas/editar_factura.html', {'form': form})

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
