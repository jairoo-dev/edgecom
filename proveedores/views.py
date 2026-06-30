from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Proveedor
from .forms import ProveedorForm
from usuarios.decoradores import permiso_requerido

@login_required(login_url='login')
@permiso_requerido('puede_ver_proveedores')
def lista_proveedores(request):
    query = request.GET.get('q', '')
    proveedores = Proveedor.objects.all().order_by('-fecha_creacion')
    if query:
        proveedores = proveedores.filter(nombre__icontains=query)
    form = ProveedorForm()
    return render(request, 'proveedores/lista_proveedores.html', {
        'proveedores': proveedores,
        'form': form,
        'query': query,
    })

@login_required(login_url='login')
@permiso_requerido('puede_ver_proveedores')
def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('lista_proveedores')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/editar_proveedor.html', {'form': form, 'proveedor': proveedor})

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('lista_proveedores')
    return render(request, 'proveedores/eliminar_proveedor.html', {'proveedor': proveedor})

@login_required(login_url='login')
def crear_proveedor_rapido(request):
    if request.method == 'POST':
        nombre   = request.POST.get('nombre', '').strip()
        rfc      = request.POST.get('rfc', '').strip()
        contacto = request.POST.get('contacto', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email    = request.POST.get('email', '').strip()

        if not nombre:
            return JsonResponse({'success': False, 'error': 'El nombre es obligatorio.'})

        proveedor = Proveedor.objects.create(
            nombre=nombre,
            rfc=rfc or None,
            contacto=contacto or None,
            telefono=telefono or None,
            email=email or None,
        )
        return JsonResponse({
            'success': True,
            'id': proveedor.pk,
            'nombre': proveedor.nombre,
        })
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})
