from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CuentaBancariaForm
from .models import CuentaBancaria

@login_required(login_url='login')
def lista_cuentas(request):
    cuentas = CuentaBancaria.objects.all().order_by('-fecha_creacion')
    form = CuentaBancariaForm()
    return render(request, 'cuentas/lista_cuentas.html', {'cuentas': cuentas, 'form': form})

@login_required(login_url='login')
def agregar_cuenta(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('sin_acceso')
    if request.method == 'POST':
        form = CuentaBancariaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cuentas')
        else:
            cuentas = CuentaBancaria.objects.all().order_by('-fecha_creacion')
            return render(request, 'cuentas/lista_cuentas.html', {
                'cuentas': cuentas,
                'form': form,
                'abrir_modal': True,
            })
    return redirect('lista_cuentas')

@login_required(login_url='login')
def editar_cuenta(request, pk):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('sin_acceso')
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
def eliminar_cuenta(request, pk):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('sin_acceso')
    cuenta = get_object_or_404(CuentaBancaria, pk=pk)
    if request.method == 'POST':
        cuenta.delete()
        return redirect('lista_cuentas')
    return render(request, 'cuentas/eliminar_cuenta.html', {'cuenta': cuenta})
