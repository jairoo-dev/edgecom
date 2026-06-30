from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
import os

from .models import Compra, OrdenCompra, DetalleOrdenCompra
from .forms import CompraForm, OrdenCompraForm
from productos.models import Producto
from configuracion.models import ConfiguracionEmpresa
from usuarios.decoradores import permiso_requerido

# ── COMPRAS ──────────────────────────────────────────────────────────────────

@login_required(login_url='login')
@permiso_requerido('puede_ver_compras')
def lista_compras(request):
    status_filtro = request.GET.get('status', '')
    compras = Compra.objects.select_related('proveedor').all()
    if status_filtro:
        compras = compras.filter(status=status_filtro)
    form = CompraForm()
    saldo_total = sum(c.saldo_pendiente() for c in compras)
    return render(request, 'compras/lista_compras.html', {
        'compras': compras,
        'form': form,
        'status_filtro': status_filtro,
        'saldo_total': saldo_total,
    })

@login_required(login_url='login')
@permiso_requerido('puede_ver_compras')
def agregar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.creado_por = request.user
            compra.save()
    return redirect('lista_compras')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_compra(request, folio):
    compra = get_object_or_404(Compra, folio=folio)
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            return redirect('lista_compras')
    else:
        form = CompraForm(instance=compra)
    return render(request, 'compras/editar_compra.html', {'form': form, 'compra': compra})

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_compra(request, folio):
    compra = get_object_or_404(Compra, folio=folio)
    if request.method == 'POST':
        compra.delete()
        return redirect('lista_compras')
    return render(request, 'compras/eliminar_compra.html', {'compra': compra})

@login_required(login_url='login')
def buscar_compras(request):
    compras = []
    proveedor_nombre = ''
    saldo_total = 0
    if request.method == 'POST':
        proveedor_nombre = request.POST.get('proveedor', '')
        if proveedor_nombre:
            compras = Compra.objects.filter(proveedor__nombre__icontains=proveedor_nombre)
            saldo_total = sum(c.saldo_pendiente() for c in compras)
    return render(request, 'compras/buscar_compras.html', {
        'compras': compras,
        'proveedor_nombre': proveedor_nombre,
        'saldo_total': saldo_total,
    })

# ── ÓRDENES DE COMPRA ─────────────────────────────────────────────────────────

@login_required(login_url='login')
@permiso_requerido('puede_ver_compras')
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.select_related('proveedor', 'usuario_solicita', 'autorizado_por').all()
    form = OrdenCompraForm()
    productos = Producto.objects.all()
    return render(request, 'compras/lista_ordenes.html', {
        'ordenes': ordenes,
        'form': form,
        'productos': productos,
    })

@login_required(login_url='login')
@permiso_requerido('puede_ver_compras')
def agregar_orden(request):
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.usuario_solicita = request.user
            orden.save()

            skus         = request.POST.getlist('sku[]')
            descripciones= request.POST.getlist('descripcion[]')
            cantidades   = request.POST.getlist('cantidad[]')
            costos       = request.POST.getlist('costo_unitario[]')
            subtotales   = request.POST.getlist('subtotal[]')

            total = 0
            for i in range(len(skus)):
                if skus[i]:
                    sub = float(subtotales[i]) if subtotales[i] else 0
                    total += sub
                    DetalleOrdenCompra.objects.create(
                        orden=orden,
                        sku=skus[i],
                        descripcion=descripciones[i],
                        cantidad=cantidades[i],
                        costo_unitario=costos[i],
                        subtotal=sub,
                    )
            orden.total = total
            orden.save()
    return redirect('lista_ordenes')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_orden(request, folio):
    orden = get_object_or_404(OrdenCompra, folio_orden=folio)
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST, instance=orden)
        if form.is_valid():
            orden = form.save()
            orden.detalles.all().delete()

            skus         = request.POST.getlist('sku[]')
            descripciones= request.POST.getlist('descripcion[]')
            cantidades   = request.POST.getlist('cantidad[]')
            costos       = request.POST.getlist('costo_unitario[]')
            subtotales   = request.POST.getlist('subtotal[]')

            total = 0
            for i in range(len(skus)):
                if skus[i]:
                    sub = float(subtotales[i]) if subtotales[i] else 0
                    total += sub
                    DetalleOrdenCompra.objects.create(
                        orden=orden,
                        sku=skus[i],
                        descripcion=descripciones[i],
                        cantidad=cantidades[i],
                        costo_unitario=costos[i],
                        subtotal=sub,
                    )
            orden.total = total
            orden.save()
            return redirect('lista_ordenes')
    else:
        form = OrdenCompraForm(instance=orden)
    detalles = orden.detalles.all()
    productos = Producto.objects.all()
    return render(request, 'compras/editar_orden.html', {'form': form, 'orden': orden, 'detalles': detalles, 'productos': productos})

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_orden(request, folio):
    orden = get_object_or_404(OrdenCompra, folio_orden=folio)
    if request.method == 'POST':
        orden.delete()
        return redirect('lista_ordenes')
    return render(request, 'compras/eliminar_orden.html', {'orden': orden})

@login_required(login_url='login')
def generar_pdf_orden(request, folio):
    orden = get_object_or_404(OrdenCompra, folio_orden=folio)
    detalles = orden.detalles.all()
    empresa = ConfiguracionEmpresa.objects.first()

    # Mismo patrón que cotizaciones: primero intenta logo de empresa, luego el estático
    if empresa and empresa.logo:
        logo_raw = os.path.join(settings.MEDIA_ROOT, str(empresa.logo))
    else:
        logo_raw = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'logo.png')
    logo_path = 'file:///' + logo_raw.replace('\\', '/').replace('\\', '/')

    html_string = render_to_string('compras/pdf_orden_compra.html', {
        'orden': orden,
        'detalles': detalles,
        'empresa': empresa,
        'logo_path': logo_path,
    })

    pdf = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{folio}.pdf"'
    return response
