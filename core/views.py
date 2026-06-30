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

    if request.user.is_superuser or request.user.is_staff:
        facturas_qs = Factura.objects.all()
        cotizaciones_qs = Cotizacion.objects.all()
    else:
        facturas_qs = Factura.objects.filter(creado_por=request.user)
        cotizaciones_qs = Cotizacion.objects.filter(creado_por=request.user)

    total_facturas = facturas_qs.count()
    total_cotizaciones = cotizaciones_qs.count()
    total_facturado = facturas_qs.aggregate(Sum('total'))['total__sum'] or 0
    ultimas_facturas = facturas_qs.order_by('-folio')[:5]
    ultimas_cotizaciones = cotizaciones_qs.order_by('-folio')[:5]

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

