from django.urls import path
from . import views

app_name = 'configuracion'

urlpatterns = [
    path('', views.lista_empresas, name='lista_empresas'),
    path('nueva/', views.crear_empresa, name='crear_empresa'),
    path('editar/<int:pk>/', views.editar_empresa, name='editar_empresa'),
]