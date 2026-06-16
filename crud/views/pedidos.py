from django.shortcuts import (
    render,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from ..models import Pedido


@login_required
def seguimiento_pedido(request, pedido_id):

    pedido = get_object_or_404(
        Pedido.objects.prefetch_related("detalles__producto"),
        id=pedido_id,
        usuario=request.user
    )

    return render(
        request,
        "crud/account/seguimiento_pedido.html",
        {
            "pedido": pedido
        }
    )