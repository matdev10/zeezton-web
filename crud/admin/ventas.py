from django.contrib import admin

from crud.models import (
    Venta,
    DetalleVenta,
)

from .utils import dinero


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

    readonly_fields = (
        "subtotal",
    )


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cliente",
        "tipo_documento",
        "total_admin",
        "fecha",
    )

    list_filter = (
        "tipo_documento",
        "fecha",
    )

    search_fields = (
        "cliente__nombre",
        "cliente__apellido",
        "cliente__numero_documento",
    )

    readonly_fields = (
        "total",
        "fecha",
    )

    ordering = ("-fecha",)

    inlines = [
        DetalleVentaInline
    ]

    def total_admin(self, obj):
        return dinero(obj.total)

    total_admin.short_description = "Total"
    total_admin.admin_order_field = "total"


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):

    list_display = (
        "venta",
        "producto",
        "cantidad",
        "precio_unitario_admin",
        "subtotal_admin",
    )

    search_fields = (
        "producto__nombre",
        "venta__cliente__nombre",
        "venta__cliente__apellido",
    )

    list_filter = (
        "venta__fecha",
    )

    ordering = ("-venta__fecha",)

    def precio_unitario_admin(self, obj):
        return dinero(obj.precio_unitario)

    precio_unitario_admin.short_description = "Precio unit."

    def subtotal_admin(self, obj):
        return dinero(obj.subtotal)

    subtotal_admin.short_description = "Subtotal"