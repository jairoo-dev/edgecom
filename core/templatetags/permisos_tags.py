from django import template
from usuarios.permisos import usuario_tiene_permiso

register = template.Library()

@register.simple_tag
def tiene_permiso(user, permiso):
    """
    Indica si el usuario tiene el permiso indicado en su rol.

    Uso en template:
        {% load permisos_tags %}
        {% tiene_permiso request.user 'puede_ver_clientes' as puede_clientes %}
        {% if puede_clientes %}
            ...mostrar link...
        {% endif %}
    """
    return usuario_tiene_permiso(user, permiso)
