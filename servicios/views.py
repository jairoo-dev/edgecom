from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from usuarios.decoradores import permiso_requerido
from .forms import ServicioForm
from .models import Servicio

@login_required(login_url='login')
@permiso_requerido('puede_ver_servicios')
def lista_servicios(request):
    servicios = Servicio.objects.all().order_by('-fecha_creacion')
    form = ServicioForm()
    return render(request, 'servicios/lista_servicios.html', {'servicios': servicios, 'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_ver_servicios')
def agregar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_servicios')
        else:
            servicios = Servicio.objects.all().order_by('-fecha_creacion')
            return render(request, 'servicios/lista_servicios.html', {
                'servicios': servicios,
                'form': form,
                'abrir_modal': True,
            })
    return redirect('lista_servicios')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_servicio(request, sku):
    servicio = get_object_or_404(Servicio, sku=sku)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('lista_servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'servicios/editar_servicio.html', {'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_servicio(request, sku):
    servicio = get_object_or_404(Servicio, sku=sku)
    if request.method == 'POST':
        servicio.delete()
        return redirect('lista_servicios')
    return render(request, 'servicios/eliminar_servicio.html', {'servicio': servicio})

@login_required(login_url='login')
def crear_rapido(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            return JsonResponse({
                'success': True,
                'sku': servicio.sku,
                'clave_sat': servicio.clave_sat,
                'unidad_sat': servicio.unidad_sat,
                'descripcion': servicio.descripcion,
                'precio_unitario': str(servicio.precio_unitario),
            })
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})
