from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FacturaForm
from .models import Factura
from usuarios.decoradores import permiso_requerido

@login_required(login_url='login')
@permiso_requerido('puede_ver_facturas')
def lista_facturas(request):
    status_filtro = request.GET.get('status', '')
    # Administradores y staff ven todas; los demás solo las suyas
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
            factura.creado_por = request.user  # asignamos el usuario automáticamente
            factura.save()
            return redirect('lista_facturas')
    return redirect('lista_facturas')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_factura(request, folio):
    factura = get_object_or_404(Factura, folio=folio)
    # Solo el creador o admin puede editar
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
    # Solo el creador o admin puede eliminar
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
    if request.method == 'POST':
        rfc = request.POST.get('rfc', '')
        if rfc:
            if request.user.is_superuser or request.user.is_staff:
                facturas = Factura.objects.filter(rfc=rfc)
            else:
                facturas = Factura.objects.filter(rfc=rfc, creado_por=request.user)
            saldo_total = sum(f.saldo_pendiente() for f in facturas)
    return render(request, 'facturas/buscar_facturas.html', {'facturas': facturas, 'rfc': rfc, 'saldo_total': saldo_total})
