from django.contrib import admin

from crud.models import Suscriptor


@admin.register(Suscriptor)
class SuscriptorAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "nombre",
        "marca",
        "modelo",
        "activo",
        "creado",
    )

    search_fields = (
        "email",
        "nombre",
        "marca",
        "modelo",
    )

    list_filter = (
        "activo",
        "marca",
        "creado",
    )

    ordering = ("-creado",)