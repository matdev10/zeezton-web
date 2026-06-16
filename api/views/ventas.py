from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from crud.models import DetalleVenta
from crud.services.ventas import crear_venta_pos


@csrf_exempt
def crear_venta(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        venta = crear_venta_pos(data)

        return JsonResponse({
            "mensaje": "Venta creada correctamente",
            "venta_id": venta.id,
            "cliente_id": venta.cliente.id,
            "total": int(venta.total),
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)












def api_detalle_ventas(request):
    try:
        detalles = DetalleVenta.objects.select_related(
            "venta",
            "venta__cliente",
            "producto"
        ).order_by("-id")

        data = []

        for d in detalles:
            cliente = d.venta.cliente if d.venta else None
            producto = d.producto

            if cliente:
                nombre_cliente = f"{cliente.nombre or ''} {cliente.apellido or ''}".strip()

                if not nombre_cliente:
                    nombre_cliente = cliente.numero_documento or "Cliente sin nombre"
            else:
                nombre_cliente = "Cliente sin registrar"

            data.append({
                "id": d.id,
                "venta_id": d.venta.id if d.venta else "",
                "fecha": d.venta.fecha.strftime("%d-%m-%Y %H:%M") if d.venta and d.venta.fecha else "",
                "tipo_documento": d.venta.tipo_documento if d.venta else "",
                "cliente": nombre_cliente,
                "producto": producto.nombre if producto else "Producto eliminado",
                "cantidad": d.cantidad,
                "precio_unitario": int(d.precio_unitario or 0),
                "subtotal": int(d.subtotal or 0),
                "total_venta": int(d.venta.total or 0) if d.venta else 0,
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




from crud.models import Venta, DetalleVenta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def eliminar_venta_prueba(request, venta_id):

    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    try:
        venta = Venta.objects.filter(
            id=venta_id
        ).first()

        if not venta:
            return JsonResponse(
                {"error": "Venta no encontrada"},
                status=404
            )

        DetalleVenta.objects.filter(
            venta=venta
        ).delete()

        venta.delete()

        return JsonResponse({
            "mensaje": "Venta eliminada"
        })

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )







@csrf_exempt
def vender_producto(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        producto_id = data.get("producto_id")
        cantidad = int(data.get("cantidad", 0))

        if not producto_id or cantidad <= 0:
            return JsonResponse({"error": "Datos incompletos o cantidad inválida"}, status=400)

        producto = Producto.objects.select_for_update().get(id=producto_id)

        if producto.stock < cantidad:
            return JsonResponse({"error": "Stock insuficiente"}, status=400)

        producto.stock -= cantidad
        producto.save(update_fields=["stock"])

        return JsonResponse({
            "mensaje": "Venta realizada correctamente",
            "nuevo_stock": producto.stock
        })

    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)