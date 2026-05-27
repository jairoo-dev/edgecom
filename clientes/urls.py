from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('editar/<str:rfc>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar/<str:rfc>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('documento/subir/<str:rfc>/', views.subir_documento, name='subir_documento'),
    path('documento/eliminar/<int:pk>/', views.eliminar_documento, name='eliminar_documento'),
]
