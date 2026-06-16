from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from django.contrib.auth import (
    authenticate,
    login,
)

from django.contrib.auth.decorators import login_required

from ..models import (
    Favorito,
    PerfilUsuario,
    Pedido,
    DireccionEntrega,
)

from ..forms import (
    RegistroUsuarioForm,
    DireccionEntregaForm,
)


# =========================================================
# LOGIN / INVITADO
# =========================================================

def login_usuario(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            request.session.pop("invitado", None)
            request.session.modified = True

            return redirect("home")

        messages.error(request, "Usuario o contraseña incorrectos.")
        request.session["abrir_login"] = True
        request.session.modified = True

        return redirect("home")

    return redirect("home")


def continuar_como_invitado(request):

    request.session["invitado"] = True
    request.session.modified = True

    return redirect("product")


def salir_invitado(request):

    request.session.pop("invitado", None)
    request.session.modified = True

    return redirect("home")


# =========================================================
# PERFIL USUARIO
# =========================================================

@login_required
def perfil_usuario(request):

    perfil, creado = PerfilUsuario.objects.get_or_create(
        usuario=request.user
    )

    favoritos = Favorito.objects.filter(
        usuario=request.user
    ).select_related(
        "producto"
    )

    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).order_by("-creado")

    context = {
        "perfil": perfil,
        "favoritos": favoritos,
        "pedidos": pedidos,
    }

    return render(
        request,
        "crud/account/perfil_mi_cuenta.html",
        context
    )


@login_required
def lista_favoritos(request):

    favoritos = Favorito.objects.filter(
        usuario=request.user
    ).select_related(
        "producto",
        "producto__marca"
    ).prefetch_related(
        "producto__imagenes"
    )

    context = {
        "favoritos": favoritos
    }

    return render(
        request,
        "crud/account/perfil_mis_favoritos.html",
        context
    )


@login_required
def mis_pedidos(request):

    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).prefetch_related(
        "detalles__producto"
    ).order_by("-creado")

    return render(
        request,
        "crud/account/perfil_mis_pedidos.html",
        {
            "pedidos": pedidos
        }
    )


# =========================================================
# DIRECCIONES
# =========================================================

@login_required
def direccion_entrega(request):

    if request.method == "POST":

        form = DireccionEntregaForm(request.POST)

        if form.is_valid():

            direccion = form.save(commit=False)
            direccion.usuario = request.user

            if not DireccionEntrega.objects.filter(
                usuario=request.user
            ).exists():
                direccion.predeterminada = True

            direccion.save()

            return redirect("direccion_entrega")

        print(form.errors)

    else:
        form = DireccionEntregaForm()

    direcciones = DireccionEntrega.objects.filter(
        usuario=request.user
    ).order_by(
        "-predeterminada",
        "-creado"
    )

    return render(
        request,
        "crud/account/perfil_mis_direcciones.html",
        {
            "form": form,
            "direcciones": direcciones,
        }
    )


@login_required
def eliminar_direccion(request, direccion_id):

    direccion = get_object_or_404(
        DireccionEntrega,
        id=direccion_id,
        usuario=request.user
    )

    direccion.delete()

    return redirect("direccion_entrega")


@login_required
def direccion_predeterminada(request, direccion_id):

    direccion = get_object_or_404(
        DireccionEntrega,
        id=direccion_id,
        usuario=request.user
    )

    DireccionEntrega.objects.filter(
        usuario=request.user
    ).update(
        predeterminada=False
    )

    direccion.predeterminada = True
    direccion.save()

    return redirect("direccion_entrega")


# =========================================================
# REGISTRO USUARIO
# =========================================================

def registro_usuario(request):

    if request.method == "POST":

        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            login(request, usuario)

            request.session.pop("invitado", None)
            request.session.modified = True

            return redirect("perfil_usuario")

    else:
        form = RegistroUsuarioForm()

    return render(
        request,
        "crud/account/registro.html",
        {
            "form": form
        }
    )