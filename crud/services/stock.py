from django.db import transaction
from django.core.exceptions import ValidationError

from ..models import Pedido, Producto


def descontar_stock_pedido(pedido):

    if pedido.stock_descontado:
        return

    with transaction.atomic():

        pedido = Pedido.objects.select_for_update().get(
            id=pedido.id
        )

        if pedido.stock_descontado:
            return

        for detalle in pedido.detalles.select_related("producto"):

            producto = Producto.objects.select_for_update().get(
                id=detalle.producto.id
            )

            if producto.stock < detalle.cantidad:
                raise ValidationError(
                    f"No hay stock suficiente para {producto.nombre}"
                )

            producto.stock -= detalle.cantidad

            producto.save(update_fields=["stock"])

        pedido.stock_descontado = True

        pedido.save(update_fields=["stock_descontado"])