from ..models import Pedido
from .stock import descontar_stock_pedido


def confirmar_pago_pedido(pedido, payment_id=None, estado_pago=None):

    pedido.mercadopago_id = payment_id
    pedido.estado_pago = estado_pago or "approved"
    pedido.estado = "PAGADO"
    pedido.save()

    descontar_stock_pedido(pedido)

    return pedido