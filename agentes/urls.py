from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_agentes, name='lista_agentes'),
    path('agregar/', views.agregar_agente, name='agregar_agente'),
    path('editar/<int:pk>/', views.editar_agente, name='editar_agente'),
    path('eliminar/<int:pk>/', views.eliminar_agente, name='eliminar_agente'),
]