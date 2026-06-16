from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from crud.models import (
    Marca,
    Producto,
    Categoria,
    Subcategoria,
    ImagenProducto,
    Reseña,
)

from .utils import dinero


# =========================
# INLINES
# =========================

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ("preview", "imagen", "principal", "orden")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj and obj.imagen:
            return format_html(
                '<img src="{}" style="width:70px;height:70px;object-fit:cover;border-radius:12px;border:1px solid rgba(15,207,217,.35);" />',
                obj.imagen.url
            )
        return "Sin imagen"

    preview.short_description = "Vista"


class ReseñaInline(admin.TabularInline):
    model = Reseña
    extra = 0
    fields = ("nombre", "email", "comentario", "calificacion", "aprobada", "creado")
    readonly_fields = ("creado",)


# =========================
# MARCAS
# =========================

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "creado", "actualizado")
    search_fields = ("nombre",)
    ordering = ("nombre",)


# =========================
# CATEGORÍAS
# =========================

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "creado", "actualizado")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria", "creado", "actualizado")
    list_filter = ("categoria",)
    search_fields = ("nombre", "categoria__nombre")
    ordering = ("categoria", "nombre")


# =========================
# PRODUCTOS
# =========================

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    actions = None
    inlines = [ImagenProductoInline, ReseñaInline]

    list_display = (
        "miniatura",
        "nombre",
        "marca",
        "precio_admin",
        "stock_admin",
        "ganancia_admin",
        "estado_comercial",
    )

    list_display_links = ("miniatura", "nombre")

    list_filter = (
        "marca",
        "categoria",
        "subcategoria",
        "oferta",
        "super_oferta",
        "destacado",
    )

    search_fields = (
        "nombre",
        "descripcion",
        "marca__nombre",
        "categoria__nombre",
        "subcategoria__nombre",
    )

    ordering = ("-id",)
    list_per_page = 100

    readonly_fields = (
        "preview_producto",
        "ganancia_unitaria",
        "ganancia_total_stock",
        "creado",
        "actualizado",
    )

    class Media:
        css = {
            "all": ("core/admin/admin_producto.css",)
        }

    fieldsets = (
        ("1. Datos visibles en el catálogo", {
            "description": "Información principal que verá el cliente cuando revise este producto en la tienda.",
            "fields": (
                "preview_producto",
                "nombre",
                "descripcion",
                "marca",
                "categoria",
                "subcategoria",
                "imagen",
            )
        }),
        ("2. Precio y rentabilidad", {
            "description": "Define el precio de venta, el costo promedio y revisa la ganancia estimada.",
            "fields": (
                "precio",
                "costo_promedio",
                "ganancia_unitaria",
                "ganancia_total_stock",
            )
        }),
        ("3. Inventario y orden en la tienda", {
            "description": "Controla el stock disponible y el orden en que aparecerá el producto en el catálogo.",
            "fields": (
                "stock",
                "orden",
                "orden_destacado",
            )
        }),
        ("4. Promociones y visibilidad", {
            "description": "Activa si el producto aparecerá como oferta, super oferta o producto destacado.",
            "fields": (
                "oferta",
                "super_oferta",
                "destacado",
                "calificacion",
            )
        }),
        ("5. Información interna del sistema", {
            "description": "Fechas generadas automáticamente por el sistema.",
            "fields": (
                "creado",
                "actualizado",
            ),
            "classes": ("collapse",),
        }),
    )

    def estado_comercial(self, obj):
        estados = []

        if obj.destacado:
            estados.append("Destacado")

        if obj.oferta:
            estados.append("Oferta")

        if obj.super_oferta:
            estados.append("Super oferta")

        if not estados:
            return "Normal"

        return " · ".join(estados)

    estado_comercial.short_description = "Estado"

    def miniatura(self, obj):
        principal = obj.imagenes.filter(principal=True).first()

        if principal and principal.imagen:
            imagen = principal.imagen.url
        elif obj.imagen:
            imagen = obj.imagen.url
        else:
            imagen = None

        if imagen:
            return format_html(
                '<img src="{}" style="width:54px;height:54px;object-fit:cover;border-radius:14px;border:1px solid rgba(15,207,217,.35);box-shadow:0 0 14px rgba(15,207,217,.20);" />',
                imagen
            )

        return mark_safe(
            '<span style="display:inline-flex;width:54px;height:54px;border-radius:14px;align-items:center;justify-content:center;background:#101722;color:#9ca8ba;border:1px solid rgba(255,255,255,.08);font-size:11px;">Sin foto</span>'
        )

    miniatura.short_description = "Imagen"

    def preview_producto(self, obj):
        if not obj or not obj.pk:
            return "Guarda el producto para ver la vista previa."

        principal = obj.imagenes.filter(principal=True).first()

        if principal and principal.imagen:
            imagen = principal.imagen.url
        elif obj.imagen:
            imagen = obj.imagen.url
        else:
            imagen = None

        if imagen:
            return format_html(
                '<img src="{}" style="width:180px;height:180px;object-fit:cover;border-radius:22px;border:1px solid rgba(15,207,217,.35);box-shadow:0 0 24px rgba(15,207,217,.18);" />',
                imagen
            )

        return "Sin imagen disponible"

    preview_producto.short_description = "Vista previa"

    def precio_admin(self, obj):
        return dinero(obj.precio or 0)

    precio_admin.short_description = "Precio"
    precio_admin.admin_order_field = "precio"

    def stock_admin(self, obj):
        stock = obj.stock or 0

        if stock <= 0:
            color = "#ff4d6d"
            texto = "Sin stock"
        elif stock <= 3:
            color = "#f4c542"
            texto = f"Stock bajo ({stock})"
        else:
            color = "#5be06b"
            texto = f"Disponible ({stock})"

        return format_html(
            '<span style="color:{};font-weight:800;">● {}</span>',
            color,
            texto
        )

    stock_admin.short_description = "Stock"
    stock_admin.admin_order_field = "stock"

    def ganancia_unitaria(self, obj):
        precio = obj.precio or 0
        costo = obj.costo_promedio or 0
        return dinero(precio - costo)

    ganancia_unitaria.short_description = "Ganancia unit."

    def ganancia_total_stock(self, obj):
        precio = obj.precio or 0
        costo = obj.costo_promedio or 0
        stock = obj.stock or 0
        return dinero((precio - costo) * stock)

    ganancia_total_stock.short_description = "Ganancia stock"

    def ganancia_admin(self, obj):
        precio = obj.precio or 0
        costo = obj.costo_promedio or 0
        ganancia = precio - costo
        color = "#5be06b" if ganancia > 0 else "#ff4d6d"

        return format_html(
            '<span style="color:{};font-weight:800;">{}</span>',
            color,
            dinero(ganancia)
        )

    ganancia_admin.short_description = "Ganancia"
    ganancia_admin.admin_order_field = "precio"


# =========================
# RESEÑAS
# =========================

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "nombre",
        "email",
        "calificacion",
        "aprobada",
        "creado",
    )

    search_fields = (
        "producto__nombre",
        "nombre",
        "email",
        "comentario",
    )

    list_filter = (
        "producto",
        "calificacion",
        "aprobada",
        "creado",
    )

    list_editable = ("aprobada",)
    ordering = ("-creado",)

    actions = ["aprobar_reseñas"]

    def aprobar_reseñas(self, request, queryset):
        queryset.update(aprobada=True)

    aprobar_reseñas.short_description = "Aprobar reseñas seleccionadas"