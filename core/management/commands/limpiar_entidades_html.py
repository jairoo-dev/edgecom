"""
Comando de un solo uso: decodifica entidades HTML (&quot; &amp; &aacute; etc.)
que quedaron guardadas literalmente en descripciones de productos, servicios
y conceptos de cotizaciones (por copiar/pegar texto desde una p\u00e1gina web).

Uso:
    python manage.py limpiar_entidades_html
    python manage.py limpiar_entidades_html --aplicar   (para guardar los cambios)

Sin --aplicar solo hace un "dry run" y te muestra qu\u00e9 registros cambiar\u00edan.
"""
import html
from django.core.management.base import BaseCommand
from productos.models import Producto
from servicios.models import Servicio
from cotizaciones.models import DetalleCotizacion


class Command(BaseCommand):
    help = 'Decodifica entidades HTML mal guardadas en descripciones (productos, servicios, conceptos de cotizaciones)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--aplicar',
            action='store_true',
            help='Guarda los cambios. Sin esta bandera solo se muestra una vista previa.',
        )

    def handle(self, *args, **options):
        aplicar = options['aplicar']
        total_cambios = 0

        modelos = [
            (Producto, 'sku'),
            (Servicio, 'sku'),
            (DetalleCotizacion, 'id'),
        ]

        for modelo, campo_id in modelos:
            self.stdout.write(self.style.HTTP_INFO(f'\n--- {modelo.__name__} ---'))
            for obj in modelo.objects.all():
                original = obj.descripcion or ''
                limpio = html.unescape(original)
                if limpio != original:
                    total_cambios += 1
                    ident = getattr(obj, campo_id)
                    self.stdout.write(f'  [{ident}] "{original}"  ->  "{limpio}"')
                    if aplicar:
                        obj.descripcion = limpio
                        obj.save(update_fields=['descripcion'])

        self.stdout.write('')
        if total_cambios == 0:
            self.stdout.write(self.style.SUCCESS('No se encontraron descripciones con entidades HTML sin decodificar.'))
        elif aplicar:
            self.stdout.write(self.style.SUCCESS(f'Listo. Se corrigieron {total_cambios} registro(s).'))
        else:
            self.stdout.write(self.style.WARNING(
                f'Se encontraron {total_cambios} registro(s) por corregir. '
                f'Vuelve a correr con --aplicar para guardarlos.'
            ))
