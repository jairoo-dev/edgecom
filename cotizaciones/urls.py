from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cotizaciones, name='lista_cotizaciones'),
    path('agregar/', views.agregar_cotizacion, name='agregar_cotizacion'),
    path('editar/<str:folio>/', views.editar_cotizacion, name='editar_cotizacion'),
    path('eliminar/<str:folio>/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
    path('api/contacto/<int:pk>/', views.api_contacto, name='api_contacto'),
    path('api/producto/<str:sku>/', views.api_producto, name='api_producto'),
    path('api/cliente/<str:rfc>/', views.api_cliente, name='api_cliente'),
    path('api/agente/<int:pk>/', views.api_agente, name='api_agente'),
    path('detalle/<str:folio>/', views.detalle_cotizacion, name='detalle_cotizacion'),
    path('buscar/', views.buscar_cotizaciones, name='buscar_cotizaciones'),
    path('pdf/<str:folio>/', views.generar_pdf, name='generar_pdf'),
]