from django.http import JsonResponse
from django.views.decorators.http import require_GET

from crud.models import Pedido


@require_GET
def listar_pedidos(request):
    pedidos = (
        Pedido.objects
        .prefetch_related("detalles__producto")
        .all()
        .order_by("-creado")
    )

    data = []

    for pedido in pedidos:
        data.append({
            "id": pedido.id,
            "cliente_nombre": pedido.cliente_nombre,
            "cliente_email": pedido.cliente_email,
            "cliente_telefono": pedido.cliente_telefono,
            "metodo_entrega": pedido.metodo_entrega,
            "metodo_entrega_texto": pedido.get_metodo_entrega_display(),
            "estado": pedido.estado,
            "estado_texto": pedido.get_estado_display(),
            "transporte": pedido.transporte,
            "transporte_texto": pedido.get_transporte_display() if pedido.transporte else "",
            "codigo_seguimiento": pedido.codigo_seguimiento or "",
            "estado_pago": pedido.estado_pago,
            "subtotal": pedido.subtotal,
            "costo_envio": pedido.costo_envio,
            "total": pedido.total,
            "creado": pedido.creado.strftime("%Y-%m-%d %H:%M"),
            "actualizado": pedido.actualizado.strftime("%Y-%m-%d %H:%M"),
            "detalles": [
                {
                    "producto_id": detalle.producto.id,
                    "producto_nombre": detalle.producto.nombre,
                    "cantidad": detalle.cantidad,
                    "precio_unitario": detalle.precio_unitario,
                    "subtotal": detalle.subtotal,
                }
                for detalle in pedido.detalles.all()
            ]
        })

    return JsonResponse(data, safe=False)