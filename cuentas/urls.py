from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cuentas, name='lista_cuentas'),
    path('agregar/', views.agregar_cuenta, name='agregar_cuenta'),
    path('editar/<int:pk>/', views.editar_cuenta, name='editar_cuenta'),
    path('eliminar/<int:pk>/', views.eliminar_cuenta, name='eliminar_cuenta'),
]