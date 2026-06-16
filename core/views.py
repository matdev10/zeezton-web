from django.shortcuts import render, redirect

from crud.models import Reseña
from crud.forms import ReseñaForm


def root(request):
    return redirect("home")


def home(request):

    context = {
        "abrir_login": request.session.pop("abrir_login", False),
    }

    return render(
        request,
        "core/index.html",
        context
    )


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method == "POST":
        form = ReseñaForm(request.POST)

        if form.is_valid():
            reseña = form.save(commit=False)
            reseña.aprobada = False
            reseña.save()
            return redirect("contact")
    else:
        form = ReseñaForm()

    reseñas = Reseña.objects.filter(aprobada=True).order_by("-creado")[:5]

    return render(request, "core/contact.html", {
        "form": form,
        "reseñas": reseñas,
    })