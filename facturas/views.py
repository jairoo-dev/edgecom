from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
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
    if request.user.is_superuser or request.user.is_staff:
        facturas = Factura.objects.all()
    else:
        facturas = Factura.objects.filter(creado_por=request.user)

    if status_filtro:
        facturas = facturas.filter(status=status_filtro)

    form = FacturaForm()
    return render(request, 'facturas/lista_facturas.html', {'facturas': facturas, 'status_filtro': status_filtro, 'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_ver_facturas')
def agregar_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.creado_por = request.user
            factura.save()
            return redirect('lista_facturas')
    return redirect('lista_facturas')

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
        if request.user.is_superuser or request.user.is_staff:
            facturas = Factura.objects.filter(rfc=cliente.rfc)
        else:
            facturas = Factura.objects.filter(rfc=cliente.rfc, creado_por=request.user)
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
    if request.user.is_superuser or request.user.is_staff:
        facturas = Factura.objects.filter(rfc=rfc)
    else:
        facturas = Factura.objects.filter(rfc=rfc, creado_por=request.user)

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
