from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from ..models import (
    Producto,
    Marca,
    Categoria,
    Subcategoria,
    ModeloAuto,
    Favorito,
    Reseña,
)

from ..forms import ReseñaForm
from ..utils import quitar_tildes

# =========================================================
# CATALOGO
# =========================================================


def catalogo(request):
    return products_list(request)


def products_list(request):

    buscar = request.GET.get("buscar", "").strip()
    marca_id = request.GET.get("marca", "").strip()
    categoria_id = request.GET.get("categoria", "").strip()
    subcategoria_id = request.GET.get("subcategoria", "").strip()
    modelo_id = request.GET.get("modelo", "").strip()

    productos = Producto.objects.select_related(
        "marca",
        "categoria",
        "subcategoria",
        "modelo_auto"
    ).prefetch_related(
        "imagenes"
    ).all().order_by("-id")

    if buscar:
        texto = quitar_tildes(buscar).lower()

        productos = productos.filter(
            Q(nombre__icontains=texto) |
            Q(descripcion__icontains=texto) |
            Q(marca__nombre__icontains=texto)
        ).distinct()

    if marca_id:
        productos = productos.filter(marca_id=marca_id)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if subcategoria_id:
        productos = productos.filter(subcategoria_id=subcategoria_id)

    if modelo_id:
        productos = productos.filter(modelo_auto_id=modelo_id)

    total_resultados = productos.count()

    paginator = Paginator(productos, 16)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    productos_destacados = Producto.objects.filter(
        destacado=True
    ).prefetch_related(
        "imagenes"
    ).order_by("-orden_destacado")[:15]

    context = {
        "productos": page_obj,
        "page_obj": page_obj,

        "productos_destacados": productos_destacados,

        "marcas": Marca.objects.all(),
        "categorias": Categoria.objects.all(),
        "subcategorias": Subcategoria.objects.all(),
        "modelos": ModeloAuto.objects.all(),

        "buscar": buscar,
        "marca_seleccionada": marca_id,
        "categoria_seleccionada": categoria_id,
        "subcategoria_seleccionada": subcategoria_id,
        "modelo_seleccionado": modelo_id,

        "total_resultados": total_resultados,
    }

    return render(
        request,
        "crud/public/catalogo.html",
        context
    )

# =========================================================
# DETALLE PRODUCTO
# =========================================================

def product_detail(request, pk):

    producto = get_object_or_404(
        Producto.objects.select_related(
            "marca",
            "categoria",
            "subcategoria",
            "modelo_auto"
        ).prefetch_related(
            "imagenes",
            "reseñas"
        ),
        id=pk
    )

    imagenes = producto.imagenes.order_by(
        "-principal",
        "orden",
        "id"
    )

    imagen_principal = imagenes.first()

    reseñas = producto.reseñas.filter(
        aprobada=True
    ).order_by("-creado")

    relacionados = Producto.objects.filter(
        categoria=producto.categoria
    ).exclude(
        id=producto.id
    )[:8]

    es_favorito = False

    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(
            usuario=request.user,
            producto=producto
        ).exists()

    context = {
        "producto": producto,
        "imagenes": imagenes,
        "imagen_principal": imagen_principal,
        "reseñas": reseñas,
        "relacionados": relacionados,
        "es_favorito": es_favorito,
    }

    return render(
        request,
        "crud/public/producto_detail.html",
        context
    )

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

# =========================================================
# OFERTAS
# =========================================================

def offers(request):

    buscar = request.GET.get("buscar", "").strip()
    marca_id = request.GET.get("marca", "").strip()
    categoria_id = request.GET.get("categoria", "").strip()
    subcategoria_id = request.GET.get("subcategoria", "").strip()
    modelo_id = request.GET.get("modelo", "").strip()

    productos = Producto.objects.filter(
        oferta=True
    ).select_related(
        "marca",
        "categoria",
        "subcategoria",
        "modelo_auto"
    ).prefetch_related(
        "imagenes"
    ).order_by("-id")

    # Buscador
    if buscar:
        productos = productos.filter(
            Q(nombre__icontains=buscar) |
            Q(descripcion__icontains=buscar) |
            Q(marca__nombre__icontains=buscar)
        ).distinct()

    # Filtros
    if marca_id:
        productos = productos.filter(marca_id=marca_id)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if subcategoria_id:
        productos = productos.filter(subcategoria_id=subcategoria_id)

    if modelo_id:
        productos = productos.filter(modelo_auto_id=modelo_id)

    total_resultados = productos.count()

    # Paginación igual que Catálogo
    paginator = Paginator(productos, 16)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Carrusel de superofertas
    productos_super_ofertas = Producto.objects.filter(
        super_oferta=True
    ).select_related(
        "marca",
        "categoria",
        "subcategoria",
        "modelo_auto"
    ).prefetch_related(
        "imagenes"
    ).order_by("-id")[:15]

    context = {
        "productos": page_obj,
        "page_obj": page_obj,

        "productos_super_ofertas": productos_super_ofertas,

        "marcas": Marca.objects.all(),
        "categorias": Categoria.objects.all(),
        "subcategorias": Subcategoria.objects.all(),
        "modelos": ModeloAuto.objects.all(),

        "buscar": buscar,
        "marca_seleccionada": marca_id,
        "categoria_seleccionada": categoria_id,
        "subcategoria_seleccionada": subcategoria_id,
        "modelo_seleccionado": modelo_id,

        "total_resultados": total_resultados,
    }

    return render(
        request,
        "crud/public/ofertas.html",
        context
    )