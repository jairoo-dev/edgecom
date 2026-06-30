from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decoradores import permiso_requerido
from .forms import ClienteForm
from .models import Cliente, DocumentoCliente

@login_required(login_url='login')
@permiso_requerido('puede_ver_clientes')
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('-fecha_creacion')
    form = ClienteForm()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes, 'form': form})

@login_required(login_url='login')
@permiso_requerido('puede_ver_clientes')
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
        else:
            clientes = Cliente.objects.all().order_by('-fecha_creacion')
            return render(request, 'clientes/lista_clientes.html', {
                'clientes': clientes,
                'form': form,
                'abrir_modal': True,
            })
    return redirect('lista_clientes')

@login_required(login_url='login')
@permiso_requerido('puede_editar')
def editar_cliente(request, rfc):
    cliente = get_object_or_404(Cliente, rfc=rfc)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required(login_url='login')
@permiso_requerido('puede_eliminar')
def eliminar_cliente(request, rfc):
    cliente = get_object_or_404(Cliente, rfc=rfc)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})

@login_required(login_url='login')
def subir_documento(request, rfc):
    cliente = get_object_or_404(Cliente, rfc=rfc)
    if request.method == 'POST' and request.FILES.get('archivo'):
        DocumentoCliente.objects.create(
            cliente=cliente,
            archivo=request.FILES['archivo']
        )
    return redirect('lista_clientes')

@login_required(login_url='login')
def eliminar_documento(request, pk):
    documento = get_object_or_404(DocumentoCliente, pk=pk)
    if request.method == 'POST':
        documento.archivo.delete()
        documento.delete()
    return redirect('lista_clientes')
