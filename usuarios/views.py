from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Rol, PerfilUsuario
from .forms import RolForm, UsuarioForm

@login_required(login_url='login')
def lista_usuarios(request):
    usuarios = PerfilUsuario.objects.select_related('user', 'rol').all()
    form = UsuarioForm()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios, 'form': form})

@login_required(login_url='login')
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            PerfilUsuario.objects.create(
                user=user,
                rol=form.cleaned_data.get('rol'),
                activo=form.cleaned_data.get('activo', True)
            )
            return redirect('lista_usuarios')
    return redirect('lista_usuarios')

@login_required(login_url='login')
def editar_usuario(request, pk):
    perfil = get_object_or_404(PerfilUsuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=perfil.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            perfil.rol = form.cleaned_data.get('rol')
            perfil.activo = form.cleaned_data.get('activo', True)
            perfil.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=perfil.user, initial={
            'rol': perfil.rol,
            'activo': perfil.activo,
        })
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'perfil': perfil})

@login_required(login_url='login')
def eliminar_usuario(request, pk):
    perfil = get_object_or_404(PerfilUsuario, pk=pk)
    if request.method == 'POST':
        perfil.user.delete()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'perfil': perfil})

@login_required(login_url='login')
def lista_roles(request):
    roles = Rol.objects.all()
    form = RolForm()
    return render(request, 'usuarios/lista_roles.html', {'roles': roles, 'form': form})

@login_required(login_url='login')
def agregar_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_roles')
    return redirect('lista_roles')

@login_required(login_url='login')
def editar_rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('lista_roles')
    else:
        form = RolForm(instance=rol)
    return render(request, 'usuarios/editar_rol.html', {'form': form, 'rol': rol})

@login_required(login_url='login')
def eliminar_rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == 'POST':
        rol.delete()
        return redirect('lista_roles')
    return render(request, 'usuarios/eliminar_rol.html', {'rol': rol})