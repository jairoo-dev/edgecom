from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decoradores import permiso_requerido
from .forms import CuentaBancariaForm
from .models import CuentaBancaria

@login_required(login_url='login')
@permiso_requerido('puede_ver_cuentas')
def lista_cuentas(request):
    cuentas = CuentaBancaria.objects.all()
    form = CuentaBancariaForm()
    return render(request, 'cuentas/lista_cuentas.html', {'cuentas': cuentas, 'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_ver_cuentas')
def agregar_cuenta(request):
    if request.method == 'POST':
        form = CuentaBancariaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cuentas')
    return redirect('lista_cuentas')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_cuenta(request, pk):
    cuenta = get_object_or_404(CuentaBancaria, pk=pk)
    if request.method == 'POST':
        form = CuentaBancariaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('lista_cuentas')
    else:
        form = CuentaBancariaForm(instance=cuenta)
    return render(request, 'cuentas/editar_cuenta.html', {'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_cuenta(request, pk):
    cuenta = get_object_or_404(CuentaBancaria, pk=pk)
    if request.method == 'POST':
        cuenta.delete()
        return redirect('lista_cuentas')
    return render(request, 'cuentas/eliminar_cuenta.html', {'cuenta': cuenta})