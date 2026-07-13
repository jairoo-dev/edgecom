from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<path:sku>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<path:sku>/', views.eliminar_producto, name='eliminar_producto'),
    path('crear-rapido/', views.crear_rapido, name='crear_producto_rapido'),
]