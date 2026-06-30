def usuario_tiene_permiso(user, permiso):
    """
    Devuelve True/False según si el usuario tiene el permiso indicado en su rol.

    Reglas:
    - Superusuarios y staff siempre tienen acceso total.
    - Usuario sin perfil, sin rol, o con perfil inactivo: sin acceso.
    - En cualquier otro caso, se consulta el flag del Rol (ej. 'puede_ver_clientes').
    """
    if not getattr(user, 'is_authenticated', False):
        return False

    if user.is_superuser or user.is_staff:
        return True

    try:
        perfil = user.perfilusuario
        rol = perfil.rol
    except Exception:
        return False

    if not perfil.activo:
        return False

    if rol is None:
        return False

    return bool(getattr(rol, permiso, False))
