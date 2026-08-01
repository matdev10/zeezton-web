from django.contrib import messages
from django.shortcuts import redirect, render

from crud.forms import MensajeContactoForm


def root(request):
    return redirect("home")


def home(request):
    context = {
        "abrir_login": request.session.pop(
            "abrir_login",
            False,
        ),
    }

    return render(
        request,
        "core/index.html",
        context,
    )


def about(request):
    return render(
        request,
        "core/about.html",
    )


def contact(request):
    if request.method == "POST":
        form = MensajeContactoForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                (
                    "Tu mensaje fue enviado correctamente. "
                    "Nos comunicaremos contigo a la brevedad."
                ),
            )

            return redirect("contact")

    else:
        form = MensajeContactoForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "core/contact.html",
        context,
    )