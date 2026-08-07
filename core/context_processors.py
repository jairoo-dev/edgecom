from configuracion.models import ConfiguracionEmpresa 

def datos_empresa(request):
    try:
        empresa = ConfiguracionEmpresa.objects.first()
    except ConfiguracionEmpresa.DoesNotExist:
        empresa = None
    return {'empresa': empresa}