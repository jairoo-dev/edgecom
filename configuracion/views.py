from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ConfiguracionEmpresa
from .forms import ConfiguracionEmpresaForm

@login_required(login_url='login')
def lista_empresas(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('sin_acceso')
    
    empresas = ConfiguracionEmpresa.objects.all()
    return render(request, 'configuracion/lista_empresas.html', {'empresas': empresas})

@login_required(login_url='login')
def crear_empresa(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('sin_acceso')
    
    if request.method == 'POST':
        form = ConfiguracionEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('configuracion:lista_empresas')
    else:
        form = ConfiguracionEmpresaForm()
    
    return render(request, 'configuracion/form_empresa.html', {'form': form, 'titulo': 'Nueva Empresa'})

@login_required(login_url='login')
def editar_empresa(request, pk):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('sin_acceso')
    
    empresa = get_object_or_404(ConfiguracionEmpresa, pk=pk)
    
    if request.method == 'POST':
        form = ConfiguracionEmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('configuracion:lista_empresas')
    else:
        form = ConfiguracionEmpresaForm(instance=empresa)
    
    return render(request, 'configuracion/form_empresa.html', {'form': form, 'titulo': 'Editar Empresa', 'empresa': empresa})