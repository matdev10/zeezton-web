from django.contrib import admin
from crud.models import TarifaEnvio


@admin.register(TarifaEnvio)
class TarifaEnvioAdmin(admin.ModelAdmin):
    list_display = (
        "comuna",
        "costo",
        "activo",
        "actualizado",
    )

    list_editable = (
        "costo",
        "activo",
    )

    search_fields = (
        "comuna",
    )

    list_filter = (
        "activo",
    )

    ordering = (
        "comuna",
    )