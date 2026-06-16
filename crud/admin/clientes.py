from django.contrib import admin

from crud.models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "numero_documento",
        "nombre_completo",
        "telefono",
        "email",
        "comuna",
        "creado",
    )

    search_fields = (
        "numero_documento",
        "nombre",
        "apellido",
        "rut",
        "telefono",
        "email",
        "comuna",
    )

    list_filter = (
        "comuna",
        "creado",
    )

    readonly_fields = (
        "creado",
        "actualizado",
    )

    ordering = ("-creado",)

    fieldsets = (
        ("Información del cliente", {
            "fields": (
                "nombre",
                "apellido",
                "fecha_nacimiento",
                "rut",
                "email",
                "telefono",
                "numero_documento",
            )
        }),
        ("Información de entrega", {
            "fields": (
                "direccion",
                "numero",
                "comuna",
                "departamento",
                "informacion_adicional",
            )
        }),
        ("Fechas del sistema", {
            "fields": (
                "creado",
                "actualizado",
            ),
            "classes": ("collapse",),
        }),
    )

    def nombre_completo(self, obj):
        return f"{obj.nombre or ''} {obj.apellido or ''}".strip()

    nombre_completo.short_description = "Cliente"