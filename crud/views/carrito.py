from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from crud.models import (
    TarifaEnvio,
    DireccionEntrega,
)
from ..models import Producto


# =========================================================
# CARRITO
# =========================================================

def ver_carrito(request):
    tipo_cliente = request.session.get(
        "tipo_cliente",
        "usuario" if request.user.is_authenticated else "invitado"
    )

    carrito = request.session.get("carrito", {})

    productos = []
    subtotal_carrito = 0
    carrito_limpio = {}

    for producto_id, item in carrito.items():
        producto = get_object_or_404(
            Producto,
            id=producto_id
        )

        if isinstance(item, dict):
            cantidad = item.get("cantidad", 1)
        else:
            cantidad = item

        cantidad = int(cantidad)
        carrito_limpio[str(producto_id)] = cantidad

        subtotal = producto.precio * cantidad
        subtotal_carrito += subtotal

        productos.append({
            "producto": producto,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

    request.session["carrito"] = carrito_limpio
    request.session.modified = True

    direccion = None
    comuna = None
    costo_envio = 0

    if request.user.is_authenticated:
        direccion = DireccionEntrega.objects.filter(
            usuario=request.user,
            predeterminada=True
        ).first()

        if direccion:
            comuna = direccion.comuna
            tarifa = TarifaEnvio.objects.filter(
                comuna__iexact=comuna,
                activo=True
            ).first()

            if tarifa:
                costo_envio = tarifa.costo

    total = subtotal_carrito + costo_envio

    context = {
        "tipo_cliente": tipo_cliente,
        "productos": productos,
        "subtotal_carrito": subtotal_carrito,
        "costo_envio": costo_envio,
        "total": total,
        "direccion": direccion,
        "comuna": comuna,
    }

    return render(
        request,
        "crud/checkout/carrito.html",
        context
    )


def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.user.is_authenticated:
        request.session["tipo_cliente"] = "usuario"
    else:
        if not request.session.get("invitado"):
            messages.warning(
                request,
                "Selecciona iniciar sesión o continuar como invitado para agregar productos."
            )
            return redirect(request.META.get("HTTP_REFERER", "product"))

        request.session["tipo_cliente"] = "invitado"

    carrito = request.session.get("carrito", {})
    producto_id_str = str(producto.id)

    if producto_id_str in carrito:
        carrito[producto_id_str] += 1
    else:
        carrito[producto_id_str] = 1

    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(request, "Producto agregado correctamente.")
    return redirect(request.META.get("HTTP_REFERER", "product"))


def eliminar_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})
    producto_id = str(producto_id)

    if producto_id in carrito:
        del carrito[producto_id]

    request.session["carrito"] = carrito
    request.session.modified = True

    return redirect("ver_carrito")


def continuar_como_invitado(request):
    request.session["invitado"] = True
    request.session["tipo_cliente"] = "invitado"
    request.session.set_expiry(0)  # Se borra al cerrar el navegador

    # MEJORA: Captura el producto desde el modal e incorpóralo al carrito altiro
    producto_id = request.GET.get("producto_id")
    if producto_id:
        carrito = request.session.get("carrito", {})
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            carrito[producto_id_str] += 1
        else:
            carrito[producto_id_str] = 1
            
        request.session["carrito"] = carrito
        messages.success(request, "Continuaste como invitado y el producto se añadió al carro.")

    request.session.modified = True

    next_url = request.GET.get("next", "product")
    return redirect(next_url)


def salir_invitado(request):
    # 1. Eliminamos de forma segura las llaves de la sesión
    request.session.pop("invitado", None)
    request.session.pop("tipo_cliente", None)
    request.session.pop("carrito", None)
    
    # 2. Destruimos la sesión por completo en el servidor
    request.session.flush()
    
    # 3. Forzamos de forma explícita el guardado del estado vacío antes de movernos
    request.session.modified = True
    request.session.save()

    # 4. En vez de usar redirect a secas, puedes limpiar las cookies de sesión del navegador 
    # para que el navegador se vea obligado a redibujar el menú desde cero.
    response = redirect("home")
    
    # Esto borra el identificador de sesión del almacenamiento del navegador del cliente
    response.delete_cookie('sessionid') 
    
    return response