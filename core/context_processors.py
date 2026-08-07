from .models import Empresa  # Ajusta al nombre real de tu modelo de Empresa

def datos_empresa(request):
    # Obtiene el primer registro de la empresa configurada
    empresa = Empresa.objects.first()
    return {'empresa': empresa}