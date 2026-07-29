from django.urls import path
from . import views


urlpatterns = [

    # ==========================================================
    # PRODUCTOS
    # ==========================================================

    path('productos/', views.api_productos),
    path('productos/<int:pk>/', views.api_producto_detalle),

    path('vender/', views.vender_producto),


    # ==========================================================
    # VENTAS
    # ==========================================================

    path('ventas/', views.crear_venta),
    path(
        'ventas/<int:venta_id>/eliminar/',
        views.eliminar_venta_prueba
    ),

    path('detalle-ventas/', views.api_detalle_ventas),


    # ==========================================================
    # PEDIDOS
    # ==========================================================

    path('pedidos/', views.listar_pedidos),
    # path('pedidos/<int:pedido_id>/', views.detalle_pedido),
    # path('pedidos/<int:pedido_id>/actualizar/', views.actualizar_pedido),


    # ==========================================================
    # CLIENTES
    # ==========================================================

    path('clientes/', views.listar_clientes),
    path('clientes/crear/', views.crear_cliente),
    path('clientes/buscar/', views.buscar_cliente_rut),
    path(
        'clientes/<int:cliente_id>/eliminar/',
        views.eliminar_cliente
    ),


    # ==========================================================
    # INFORMES
    # ==========================================================

    path('informes/', views.crear_informe),
    path('informes/listar/', views.listar_informes),

]