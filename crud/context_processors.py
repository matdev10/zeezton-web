def carrito_context(request):
    # 1. Si NO está logueado Y TAMPOCO tiene la sesión de invitado activa, el carro es 0 SÍ O SÍ
    if not request.user.is_authenticated and not request.session.get("invitado"):
        return {
            "cantidad_carrito": 0
        }

    # 2. Si es un usuario real o un invitado válido, contamos normalmente
    carrito = request.session.get("carrito", {})
    total_items_carrito = 0

    for item in carrito.values():
        if isinstance(item, dict):
            total_items_carrito += int(item.get("cantidad", 0))
        else:
            total_items_carrito += int(item)

    return {
        "cantidad_carrito": total_items_carrito
    }