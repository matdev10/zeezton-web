from django.http import JsonResponse
from crud.models import Producto


def obtener_imagen_producto(request, producto):
    imagen_extra = producto.imagenes.filter(
        principal=True
    ).order_by(
        "orden",
        "id"
    ).first()

    if not imagen_extra:
        imagen_extra = producto.imagenes.order_by(
            "orden",
            "id"
        ).first()

    if imagen_extra and imagen_extra.imagen:
        return request.build_absolute_uri(imagen_extra.imagen.url)

    if producto.imagen:
        return request.build_absolute_uri(producto.imagen.url)

    return ""


def api_productos(request):
    try:
        productos = Producto.objects.select_related(
            "marca"
        ).prefetch_related(
            "imagenes"
        ).order_by("-creado")

        data = []

        for p in productos:
         data.append({
        "id": p.id,
        "nombre": p.nombre,
        "descripcion": p.descripcion or "",
        "precio": int(p.precio),
        "stock": p.stock,
        "marca": p.marca.nombre if p.marca else "",
        "imagen": obtener_imagen_producto(request, p),
        "destacado": p.destacado,
        "oferta": p.oferta,
        "super_oferta": p.super_oferta,
        "calificacion": float(p.calificacion),
        "estado_stock": getattr(p, "estado_stock", ""),
        "estado_stock_display": getattr(p, "estado_stock_display", ""),
         })
  
        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def api_producto_detalle(request, pk):
    try:
        p = Producto.objects.select_related(
            "marca"
        ).prefetch_related(
            "imagenes"
        ).get(pk=pk)

        data = {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion or "",
            "precio": int(p.precio),
            "stock": p.stock,
            "marca": p.marca.nombre if p.marca else "",
            "imagen": obtener_imagen_producto(request, p),
            "destacado": p.destacado,
            "oferta": p.oferta,
            "super_oferta": p.super_oferta,
            "calificacion": float(p.calificacion),
            "imagenes": [
    {
        "id": img.id,
        "url": request.build_absolute_uri(img.imagen.url),
        "principal": img.principal,
        "orden": img.orden,
    }
    for img in p.imagenes.order_by("-principal", "orden", "id")
    if img.imagen
],
        }

        return JsonResponse(data, safe=False)

    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
