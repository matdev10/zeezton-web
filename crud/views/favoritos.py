from django.shortcuts import (
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from ..models import (
    Producto,
    Favorito,
)
# =========================================================
# FAVORITOS
# =========================================================

@login_required
def agregar_favorito(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    favorito = Favorito.objects.filter(
        usuario=request.user,
        producto=producto
    )

    if favorito.exists():
        favorito.delete()
    else:
        Favorito.objects.create(
            usuario=request.user,
            producto=producto
        )

    return redirect(request.META.get("HTTP_REFERER", "product"))


