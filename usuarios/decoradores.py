from functools import wraps
from django.shortcuts import redirect
from .permisos import usuario_tiene_permiso

def permiso_requerido(permiso):
    """
    Decorador que verifica si el usuario tiene un permiso específico en su rol.
    
    Uso:
        @permiso_requerido('puede_ver_facturas')
        def lista_facturas(request): ...

    Si el usuario es superuser o staff, siempre tiene acceso a todo.
    Si el usuario no tiene perfil o rol asignado, se le redirige al dashboard.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Superusuarios y staff siempre tienen acceso total
            if request.user.is_superuser or request.user.is_staff:
                return view_func(request, *args, **kwargs)

            # Verificar que el usuario tiene perfil y rol asignado (para distinguir
            # 'sin perfil' de 'permiso negado' y dar el redirect correcto)
            try:
                perfil = request.user.perfilusuario
                rol = perfil.rol
            except Exception:
                return redirect('dashboard')

            if not perfil.activo:
                return redirect('logout')

            if rol is None:
                return redirect('dashboard')

            # Verificar el permiso específico (misma lógica que usuario_tiene_permiso)
            if not usuario_tiene_permiso(request.user, permiso):
                return redirect('sin_acceso')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
