from django.core.management.base import BaseCommand
from crud.models import Pedido


class Command(BaseCommand):
    help = "Elimina todos los pedidos de prueba y sus detalles."

    def handle(self, *args, **options):
        total_pedidos = Pedido.objects.count()

        if total_pedidos == 0:
            self.stdout.write(
                self.style.WARNING("No hay pedidos para eliminar.")
            )
            return

        Pedido.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Se eliminaron {total_pedidos} pedidos correctamente."
            )
        )