from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import NotRegistered


try:
    admin.site.unregister(User)

except NotRegistered:
    pass


@admin.register(User)
class UsuarioZeeztonAdmin(UserAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.exclude(is_superuser=True)

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = (
        "-date_joined",
    )