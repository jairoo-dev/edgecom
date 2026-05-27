from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decoradores import permiso_requerido
from .forms import ContactoForm
from .models import Contacto

@login_required(login_url='login')
@permiso_requerido('puede_ver_directorio')
def lista_contactos(request):
    contactos = Contacto.objects.all()
    form = ContactoForm()
    return render(request, 'directorio/lista_contactos.html', {'contactos': contactos, 'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_ver_directorio')
def agregar_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    return redirect('lista_contactos')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'directorio/editar_contacto.html', {'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        contacto.delete()
        return redirect('lista_contactos')
    return render(request, 'directorio/eliminar_contacto.html', {'contacto': contacto})