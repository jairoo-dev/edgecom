from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decoradores import permiso_requerido
from .forms import ProductoForm
from .models import Producto
from django.http import JsonResponse

@login_required(login_url='login')
@permiso_requerido('puede_ver_productos')
def lista_productos(request):
    productos = Producto.objects.all()
    form = ProductoForm()
    return render(request, 'productos/lista_productos.html', {'productos': productos, 'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_ver_productos')
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    return redirect('lista_productos')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_producto(request, sku):
    producto = get_object_or_404(Producto, sku=sku)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_producto(request, sku):
    producto = get_object_or_404(Producto, sku=sku)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})

@login_required(login_url='login')
def crear_rapido(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            return JsonResponse({
                'success': True,
                'sku': producto.sku,
                'clave_sat': producto.clave_sat,
                'unidad_sat': producto.unidad_sat,
                'descripcion': producto.descripcion,
                'precio_unitario': str(producto.precio_unitario),
            })
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})