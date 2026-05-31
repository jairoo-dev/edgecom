from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_servicios, name='lista_servicios'),
    path('agregar/', views.agregar_servicio, name='agregar_servicio'),
    path('editar/<str:sku>/', views.editar_servicio, name='editar_servicio'),
    path('eliminar/<str:sku>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('crear-rapido/', views.crear_rapido, name='crear_servicio_rapido'),
]
