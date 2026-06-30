from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decoradores import permiso_requerido
from .forms import AgenteForm
from .models import Agente

@login_required(login_url='login')
@permiso_requerido('puede_ver_agentes')
def lista_agentes(request):
    agentes = Agente.objects.all().order_by('-fecha_creacion')
    form = AgenteForm()
    return render(request, 'agentes/lista_agentes.html', {'agentes': agentes, 'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_ver_agentes')
def agregar_agente(request):
    if request.method == 'POST':
        form = AgenteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_agentes')
        else:
            agentes = Agente.objects.all().order_by('-fecha_creacion')
            return render(request, 'agentes/lista_agentes.html', {
                'agentes': agentes,
                'form': form,
                'abrir_modal': True,
            })
    return redirect('lista_agentes')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_agente(request, pk):
    agente = get_object_or_404(Agente, pk=pk)
    if request.method == 'POST':
        form = AgenteForm(request.POST, request.FILES, instance=agente)
        if form.is_valid():
            form.save()
            return redirect('lista_agentes')
    else:
        form = AgenteForm(instance=agente)
    return render(request, 'agentes/editar_agente.html', {'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_agente(request, pk):
    agente = get_object_or_404(Agente, pk=pk)
    if request.method == 'POST':
        agente.delete()
        return redirect('lista_agentes')
    return render(request, 'agentes/eliminar_agente.html', {'agente': agente})
