from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from crud.models import Pedido


@staff_member_required
def gestionar_pedido(request, pedido_id):

    pedido = get_object_or_404(
        Pedido.objects.prefetch_related("detalles__producto"),
        id=pedido_id
    )

    if request.method == "POST":
        pedido.estado = request.POST.get("estado")
        pedido.transporte = request.POST.get("transporte") or None
        pedido.codigo_seguimiento = request.POST.get("codigo_seguimiento") or None
        pedido.nota_despacho = request.POST.get("nota_despacho") or None
        pedido.save()

        messages.success(request, "Pedido actualizado correctamente.")

        return redirect("gestionar_pedido", pedido_id=pedido.id)

    return render(
    request,
    "admin/pedido_gestionar.html",
    {
        "pedido": pedido
    }
)