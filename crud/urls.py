from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from crud.views.admin.pedidos import gestionar_pedido

# IMPORTACIÓN EXPLÍCITA DE TUS VISTAS DE CHECKOUT:
from crud.views.checkout import checkout, calcular_envio_ajax

urlpatterns = [
    # =========================
    # ADMINISTRACIÓN DE PEDIDOS
    # =========================
    path(
    "admin-pedidos/<int:pedido_id>/gestionar/",
    gestionar_pedido,
    name="gestionar_pedido"
    ),

    # =========================
    # PRODUCTOS / TIENDA
    # =========================
    path("shop/", views.products_list, name="product"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("producto/<int:pk>/", views.product_detail, name="detalle_producto"),
    path("offers/", views.offers, name="offers"),

    # =========================
    # CARRITO / CHECKOUT
    # =========================
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_carrito, name="agregar_carrito"),
    path("carrito/eliminar/<int:producto_id>/", views.eliminar_carrito, name="eliminar_carrito"),
    
    # Cambiamos views.checkout por checkout directamente:
    path("checkout/", checkout, name="checkout"),
    
    # Registramos correctamente la URL apuntando directo a la función del archivo checkout.py:
    path("calcular-envio-ajax/", calcular_envio_ajax, name="calcular_envio_ajax"),

    # =========================
    # PAGOS
    # =========================
    path("pagar/<int:producto_id>/", views.pagar_producto, name="pagar_producto"),
    path("pedido/<int:pedido_id>/mercadopago/", views.pagar_pedido_mercadopago, name="pagar_pedido_mercadopago"),
    path("pago-exitoso/", views.pago_exitoso, name="pago_exitoso"),
    path("pago-fallido/", views.pago_fallido, name="pago_fallido"),
    path("pago-pendiente/", views.pago_pendiente, name="pago_pendiente"),

    # =========================
    # CUENTA
    # =========================
    path("perfil/", views.perfil_usuario, name="perfil_usuario"),
    path("registro/", views.registro_usuario, name="registro_usuario"),
    path("login/", views.login_usuario, name="login"),
    path(
    "logout/",
    auth_views.LogoutView.as_view(next_page="/"),
    name="logout"
    ),
    path("mis-pedidos/", views.mis_pedidos, name="mis_pedidos"),
    path(
    "pedido/<int:pedido_id>/seguimiento/",
    views.seguimiento_pedido,
    name="seguimiento_pedido"
    ),
    path("invitado/", views.continuar_como_invitado, name="continuar_como_invitado"),
    path("salir-invitado/", views.salir_invitado, name="salir_invitado"),

    # =========================
    # FAVORITOS
    # =========================
    path("favoritos/", views.lista_favoritos, name="lista_favoritos"),
    path("favorito/agregar/<int:producto_id>/", views.agregar_favorito, name="agregar_favorito"),

    # =========================
    # DIRECCIONES
    # =========================
    path("direccion/", views.direccion_entrega, name="direccion_entrega"),
    path("direccion/eliminar/<int:direccion_id>/", views.eliminar_direccion, name="eliminar_direccion"),
    path("direccion/predeterminada/<int:direccion_id>/", views.direccion_predeterminada, name="direccion_predeterminada"),
]

