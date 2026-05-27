from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('roles/', views.lista_roles, name='lista_roles'),
    path('roles/agregar/', views.agregar_rol, name='agregar_rol'),
    path('roles/editar/<int:pk>/', views.editar_rol, name='editar_rol'),
    path('roles/eliminar/<int:pk>/', views.eliminar_rol, name='eliminar_rol'),
]