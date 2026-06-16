from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_facturas, name='lista_facturas'),
    path('agregar/', views.agregar_factura, name='agregar_factura'),
    path('editar/<str:folio>/', views.editar_factura, name='editar_factura'),
    path('eliminar/<str:folio>/', views.eliminar_factura, name='eliminar_factura'),
    path('buscar/', views.buscar_facturas, name='buscar_facturas'),
    path('estado-cuenta/<str:rfc>/', views.estado_cuenta_pdf, name='estado_cuenta_pdf'),
]
