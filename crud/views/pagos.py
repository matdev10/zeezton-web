from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail

import mercadopago

from ..models import Producto, Pedido
from ..services import confirmar_pago_pedido


# =========================================================
# CONFIG LOCAL
# =========================================================

LOCAL_BASE_URL = "http://127.0.0.1:8000"


# =========================================================
# PAGAR PRODUCTO DIRECTO
# =========================================================

def pagar_producto(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    access_token = getattr(settings, "MERCADOPAGO_ACCESS_TOKEN", None)

    if not access_token:
        return HttpResponse("Falta configurar MERCADOPAGO_ACCESS_TOKEN")

    sdk = mercadopago.SDK(access_token)

    preference_data = {
        "items": [
            {
                "title": producto.nombre,
                "quantity": 1,
                "unit_price": int(producto.precio),
                "currency_id": "CLP",
            }
        ],
        "back_urls": {
            "success": f"{LOCAL_BASE_URL}/pago-exitoso/",
            "failure": f"{LOCAL_BASE_URL}/pago-fallido/",
            "pending": f"{LOCAL_BASE_URL}/pago-pendiente/",
        },
    }

    preference_response = sdk.preference().create(preference_data)

    if not preference_response:
        return HttpResponse("Mercado Pago no devolvió respuesta.")

    response = preference_response.get("response", {})

    init_point = response.get("init_point") or response.get("sandbox_init_point")

    if not init_point:
        return HttpResponse(f"Mercado Pago error: {preference_response}")

    return redirect(init_point)


# =========================================================
# PAGAR PEDIDO COMPLETO
# =========================================================

def pagar_pedido_mercadopago(request, pedido_id):

    pedido = get_object_or_404(
        Pedido.objects.prefetch_related("detalles__producto"),
        id=pedido_id
    )

    access_token = getattr(settings, "MERCADOPAGO_ACCESS_TOKEN", None)

    if not access_token:
        return HttpResponse("Falta configurar MERCADOPAGO_ACCESS_TOKEN")

    items = []

    for detalle in pedido.detalles.all():
        items.append({
            "title": detalle.producto.nombre,
            "quantity": int(detalle.cantidad),
            "unit_price": int(detalle.precio_unitario),
            "currency_id": "CLP",
        })

    if pedido.costo_envio and pedido.costo_envio > 0:
        items.append({
            "title": "Costo de envío",
            "quantity": 1,
            "unit_price": int(pedido.costo_envio),
            "currency_id": "CLP",
        })

    if not items:
        return HttpResponse("El pedido no tiene productos asociados.")

    sdk = mercadopago.SDK(access_token)

    preference_data = {
    "items": items,
    "external_reference": str(pedido.id),
    "back_urls": {
        "success": "http://127.0.0.1:8000/pago-exitoso/",
        "failure": "http://127.0.0.1:8000/pago-fallido/",
        "pending": "http://127.0.0.1:8000/pago-pendiente/",
    },
    "auto_return": "approved",
}
    preference_response = sdk.preference().create(preference_data)

    if not preference_response:
        return HttpResponse("Mercado Pago no devolvió respuesta.")

    response = preference_response.get("response", {})

    init_point = response.get("init_point") or response.get("sandbox_init_point")

    if not init_point:
        return HttpResponse(f"Mercado Pago error: {preference_response}")

    return redirect(init_point)


# =========================================================
# PAGO EXITOSO
# =========================================================

def pago_exitoso(request):

    payment_id = request.GET.get("payment_id")
    status = request.GET.get("status")
    external_reference = request.GET.get("external_reference")

    if external_reference:

        pedido = Pedido.objects.filter(
            id=external_reference
        ).first()

        if pedido:

            if status == "approved":

                confirmar_pago_pedido(
                    pedido,
                    payment_id=payment_id,
                    estado_pago=status
                )

                if pedido.cliente_email:
                    send_mail(
                        subject=f"Confirmación de compra Zeezton #{pedido.id}",
                        message=f"""
Hola {pedido.cliente_nombre},

Tu compra fue confirmada correctamente.

Pedido: #{pedido.id}
Total: ${pedido.total}

Gracias por comprar en Zeezton Store.
                        """,
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                        recipient_list=[pedido.cliente_email],
                        fail_silently=True,
                    )

            else:
                pedido.mercadopago_id = payment_id
                pedido.estado_pago = status
                pedido.save()

    return render(
        request,
        "crud/checkout/pago_exitoso.html"
    )


# =========================================================
# PAGO FALLIDO
# =========================================================

def pago_fallido(request):

    external_reference = request.GET.get("external_reference")

    if external_reference:

        pedido = Pedido.objects.filter(
            id=external_reference
        ).first()

        if pedido:
            pedido.estado_pago = "rejected"
            pedido.estado = "CANCELADO"
            pedido.save()

    return render(
        request,
        "crud/checkout/pago_fallido.html"
    )


# =========================================================
# PAGO PENDIENTE
# =========================================================

def pago_pendiente(request):

    external_reference = request.GET.get("external_reference")

    if external_reference:

        pedido = Pedido.objects.filter(
            id=external_reference
        ).first()

        if pedido:
            pedido.estado_pago = "pending"
            pedido.save()

    return render(
        request,
        "crud/checkout/pago_pendiente.html"
    )