from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from clientes.models import Cliente
from facturas.models import Factura
from cotizaciones.models import Cotizacion

def login_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Usuario o contraseña incorrectos'
    return render(request, 'core/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_facturas = Factura.objects.count()
    total_cotizaciones = Cotizacion.objects.count()
    total_facturado = Factura.objects.aggregate(Sum('total'))['total__sum'] or 0
    ultimas_facturas = Factura.objects.order_by('-folio')[:5]
    ultimas_cotizaciones = Cotizacion.objects.order_by('-folio')[:5]

    context = {
        'total_clientes': total_clientes,
        'total_facturas': total_facturas,
        'total_cotizaciones': total_cotizaciones,
        'total_facturado': total_facturado,
        'ultimas_facturas': ultimas_facturas,
        'ultimas_cotizaciones': ultimas_cotizaciones,
    }
    return render(request, 'core/dashboard.html', context)

@login_required(login_url='login')
def sin_acceso(request):
    return render(request, 'core/sin_acceso.html')

