from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from ..models import (
    Producto, Pedido, DetallePedido, 
    DireccionEntrega, TarifaEnvio
)

# =========================================================
# VISTA CHECKOUT: PROCESO DE COMPRA
# =========================================================
def checkout(request):
    # 1. VALIDACIÓN DE CARRITO
    carrito = request.session.get("carrito", {})
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("ver_carrito")

    # 2. PROCESAR ITEMS
    items = []
    subtotal_carrito = 0
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(cantidad)
        subtotal = producto.precio * cantidad
        subtotal_carrito += subtotal
        items.append({"producto": producto, "nombre": producto.nombre, "cantidad": cantidad, "precio": producto.precio, "subtotal": subtotal})

    # 3. LÓGICA DE ENVÍO (POST)
    costo_envio = 0
    if request.method == "POST":
        comuna_seleccionada = request.POST.get("comuna", "").strip()
        tarifa = TarifaEnvio.objects.filter(comuna__iexact=comuna_seleccionada, activo=True).first()
        if tarifa:
            costo_envio = tarifa.costo
            
        total = subtotal_carrito + costo_envio

        # 4. CREAR PEDIDO
        usuario_pedido = request.user if request.user.is_authenticated else None
        pedido = Pedido.objects.create(
            usuario=usuario_pedido,
            cliente_nombre=request.POST.get("nombre_completo"),
            cliente_email=request.POST.get("email"),
            cliente_telefono=request.POST.get("telefono"),
            subtotal=subtotal_carrito,
            costo_envio=costo_envio,
            total=total,
            estado="PENDIENTE_PAGO"
        )

        for item in items:
            DetallePedido.objects.create(
                pedido=pedido, producto=item["producto"], cantidad=item["cantidad"],
                precio_unitario=item["precio"], subtotal=item["subtotal"]
            )

        # GUARDAR ID EN SESIÓN
        request.session["pedido_id"] = pedido.id
        request.session["carrito"] = {} 

        return redirect("pagar_pedido_mercadopago", pedido_id=pedido.id)

    comunas_disponibles = TarifaEnvio.objects.filter(activo=True).order_by('comuna')
    return render(request, "crud/checkout/checkout.html", {
        "items": items, "subtotal_carrito": subtotal_carrito, 
        "comunas_disponibles": comunas_disponibles
    })

# =========================================================
# VISTA AJAX: CÁLCULO DE ENVÍO (SOLO UNA VEZ DEFINIDA)
# =========================================================
def calcular_envio_ajax(request):
    comuna_nombre = request.GET.get('comuna', '').strip()
    tarifa = TarifaEnvio.objects.filter(comuna__iexact=comuna_nombre, activo=True).first()
    costo = tarifa.costo if tarifa else 0
    return JsonResponse({'costo_envio': int(costo)})