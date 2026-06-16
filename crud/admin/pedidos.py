from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from crud.models import (
    Pedido,
    DetallePedido,
    DireccionEntrega,
)

from .utils import dinero


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

    readonly_fields = (
        "producto",
        "cantidad",
        "precio_unitario_admin",
        "subtotal_admin",
    )

    fields = (
        "producto",
        "cantidad",
        "precio_unitario_admin",
        "subtotal_admin",
    )

    can_delete = False

    def precio_unitario_admin(self, obj):
        return dinero(obj.precio_unitario)

    precio_unitario_admin.short_description = "Precio unit."

    def subtotal_admin(self, obj):
        return dinero(obj.subtotal)

    subtotal_admin.short_description = "Subtotal"


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [DetallePedidoInline]

    list_display = (
        "id",
        "cliente_nombre",
        "cliente_email",
        "metodo_entrega",
        "estado_badge",
        "transporte_badge",
        "codigo_seguimiento",
        "total_admin",
        "boton_gestionar",
        "creado",
    )

    list_display_links = (
        "id",
        "cliente_nombre",
    )

    list_filter = (
        "estado",
        "metodo_entrega",
        "transporte",
        "estado_pago",
        "creado",
    )

    search_fields = (
        "id",
        "cliente_nombre",
        "cliente_email",
        "cliente_telefono",
        "codigo_seguimiento",
        "mercadopago_id",
    )

    ordering = ("-creado",)

    readonly_fields = (
        "usuario",
        "cliente_nombre",
        "cliente_email",
        "cliente_telefono",
        "subtotal_admin",
        "total_admin",
        "mercadopago_id",
        "estado_pago",
        "stock_descontado",
        "creado",
        "actualizado",
    )

    class Media:
        css = {
            "all": (
                "core/admin/admin_pedidos.css",
            )
        }

    fieldsets = (
        ("1. Datos del cliente", {
            "fields": (
                "usuario",
                "cliente_nombre",
                "cliente_email",
                "cliente_telefono",
            )
        }),
        ("2. Estado del pedido", {
            "description": "Cambia el estado del pedido según el avance real de preparación o entrega.",
            "fields": (
                "estado",
                "metodo_entrega",
            )
        }),
        ("3. Gestión de despacho", {
            "description": "Esta información será visible para el cliente en la pantalla de seguimiento.",
            "fields": (
                "transporte",
                "codigo_seguimiento",
                "nota_despacho",
            )
        }),
        ("4. Pago Mercado Pago", {
            "classes": ("collapse",),
            "fields": (
                "mercadopago_id",
                "estado_pago",
                "stock_descontado",
            )
        }),
        ("5. Totales", {
            "fields": (
                "subtotal_admin",
                "costo_envio",
                "total_admin",
            )
        }),
        ("6. Fechas", {
            "classes": ("collapse",),
            "fields": (
                "creado",
                "actualizado",
            )
        }),
    )

    def boton_gestionar(self, obj):
        url = reverse("gestionar_pedido", args=[obj.id])

        return format_html(
            '<a class="zz-admin-action-btn" href="{}">Gestionar</a>',
            url
        )

    boton_gestionar.short_description = "Acción"

    def estado_badge(self, obj):
        colores = {
            "PENDIENTE_PAGO": "#f4c542",
            "PAGADO": "#25ff9a",
            "PREPARANDO": "#00eaff",
            "LISTO_RETIRO": "#8b5cf6",
            "ENVIADO": "#38bdf8",
            "ENTREGADO": "#22c55e",
            "CANCELADO": "#ff4d6d",
        }

        color = colores.get(obj.estado, "#ffffff")

        return format_html(
            '<span class="zz-status-badge" style="--badge-color:{};">{}</span>',
            color,
            obj.get_estado_display()
        )

    estado_badge.short_description = "Estado"
    estado_badge.admin_order_field = "estado"

    def transporte_badge(self, obj):
        if not obj.transporte:
            return format_html(
                '<span class="zz-muted-badge">Pendiente</span>'
            )

        return format_html(
            '<span class="zz-transport-badge">{}</span>',
            obj.get_transporte_display()
        )

    transporte_badge.short_description = "Transporte"
    transporte_badge.admin_order_field = "transporte"

    def subtotal_admin(self, obj):
        return dinero(obj.subtotal)

    subtotal_admin.short_description = "Subtotal"

    def total_admin(self, obj):
        return dinero(obj.total)

    total_admin.short_description = "Total"


@admin.register(DireccionEntrega)
class DireccionEntregaAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "nombre_completo",
        "telefono",
        "region",
        "comuna",
        "calle",
        "numero",
        "predeterminada",
        "creado",
    )

    list_filter = (
        "predeterminada",
        "region",
        "comuna",
    )

    search_fields = (
        "usuario__username",
        "usuario__email",
        "nombre_completo",
        "telefono",
        "region",
        "comuna",
        "calle",
        "numero",
    )

    ordering = (
        "-predeterminada",
        "-creado",
    )

    readonly_fields = (
        "creado",
        "actualizado",
    )