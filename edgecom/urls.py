from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('clientes/', include('clientes.urls')),
    path('facturas/', include('facturas.urls')),
    path('cotizaciones/', include('cotizaciones.urls')),
    path('catalogo/productos/', include('productos.urls')),
    path('catalogo/servicios/', include('servicios.urls')),
    path('directorio/', include('directorio.urls')),
    path('agentes/', include('agentes.urls')),
    path('cuentas/', include('cuentas.urls')),
    path('usuarios/', include('usuarios.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)