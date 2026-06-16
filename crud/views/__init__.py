from .productos import (
    products_list,
    product_detail,
    catalogo,
    offers,
)

from .carrito import *
from .checkout import *
from .pagos import *
from .cuenta import *
from .favoritos import *
from .pedidos import *
# Abre crud/views/__init__.py y asegúrate de tener esto:
from .pagos import pagar_producto, pagar_pedido_mercadopago, pago_exitoso, pago_fallido, pago_pendiente