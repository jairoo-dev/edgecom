from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ConfiguracionEmpresa
from .forms import ConfiguracionEmpresaForm

@login_required(login_url='login')
def configuracion(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('sin_acceso')
    
    empresa = ConfiguracionEmpresa.objects.first()
    
    if request.method == 'POST':
        if empresa:
            form = ConfiguracionEmpresaForm(request.POST, request.FILES, instance=empresa)
        else:
            form = ConfiguracionEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('configuracion')
    else:
        form = ConfiguracionEmpresaForm(instance=empresa)
    
    return render(request, 'configuracion/configuracion.html', {'form': form, 'empresa': empresa})