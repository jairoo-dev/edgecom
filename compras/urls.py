from django.urls import path
from . import views

urlpatterns = [
    # Compras (facturas recibidas)
    path('', views.lista_compras, name='lista_compras'),
    path('agregar/', views.agregar_compra, name='agregar_compra'),
    path('editar/<str:folio>/', views.editar_compra, name='editar_compra'),
    path('eliminar/<str:folio>/', views.eliminar_compra, name='eliminar_compra'),
    path('buscar/', views.buscar_compras, name='buscar_compras'),
    # Órdenes de Compra
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('ordenes/agregar/', views.agregar_orden, name='agregar_orden'),
    path('ordenes/editar/<str:folio>/', views.editar_orden, name='editar_orden'),
    path('ordenes/eliminar/<str:folio>/', views.eliminar_orden, name='eliminar_orden'),
    path('ordenes/pdf/<str:folio>/', views.generar_pdf_orden, name='pdf_orden'),
]
