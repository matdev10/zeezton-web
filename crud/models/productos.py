from django.db import models
from django.contrib.auth.models import User



# 1. MODELOS BASE


class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Subcategoria(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='subcategorias'
    )

    nombre = models.CharField(max_length=100)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        unique_together = ('categoria', 'nombre')

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"


class ModeloAuto(models.Model):
    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE,
        related_name='modelos'
    )

    nombre = models.CharField(max_length=100)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        unique_together = ('marca', 'nombre')

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"


# 2. PRODUCTOS
class Producto(models.Model):

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )

    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )

    modelo_auto = models.ForeignKey(
        ModeloAuto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )

    destacado = models.BooleanField(default=False)

    oferta = models.BooleanField(default=False)

    super_oferta = models.BooleanField(
        default=False,
        verbose_name="¿Es Super Oferta?"
    )

    precio = models.PositiveIntegerField()

    calificacion = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0
    )

    costo_promedio = models.PositiveIntegerField(default=0)

    stock = models.PositiveIntegerField(default=0)

    orden = models.PositiveIntegerField(default=0)

    orden_destacado = models.PositiveIntegerField(default=0)

    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE,
        related_name="productos"
    )

    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True
    )

    creado = models.DateTimeField(auto_now_add=True)

    actualizado = models.DateTimeField(auto_now=True)

    @property
    def estado_stock(self):
        if self.stock <= 0:
            return "SIN_STOCK"
        elif self.stock <= 2:
            return "STOCK_BAJO"
        return "DISPONIBLE"

    @property
    def estado_stock_display(self):
        estados = {
            "SIN_STOCK": "Sin stock",
            "STOCK_BAJO": "Stock bajo",
            "DISPONIBLE": "Disponible",
        }

        return estados.get(
            self.estado_stock,
            "Disponible"
        )

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return self.nombre
    



class ImagenProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='productos/galeria/')
    principal = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
    


    

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='favorito_de')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto')

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"



class Reseña(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="reseñas",
        null=True,
        blank=True
    )

    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    comentario = models.TextField()

    calificacion = models.IntegerField(
        choices=[(i, f"{i} ★") for i in range(1, 6)],
        default=5
    )

    creado = models.DateTimeField(auto_now_add=True)
    aprobada = models.BooleanField(default=False)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        if self.producto:
            return f"{self.producto.nombre} - {self.nombre} - {self.calificacion}★"
        return f"{self.nombre} - {self.calificacion}★"
    
