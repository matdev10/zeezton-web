from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .productos import Producto



# 4. PEDIDOS

class Pedido(models.Model):

    ESTADOS = [
        ("PENDIENTE_PAGO", "Pendiente de pago"),
        ("PAGADO", "Pagado"),
        ("PREPARANDO", "Preparando pedido"),
        ("LISTO_RETIRO", "Listo para retiro"),
        ("ENVIADO", "Enviado"),
        ("ENTREGADO", "Entregado"),
        ("CANCELADO", "Cancelado"),
    ]

    METODOS_ENTREGA = [
        ("RETIRO", "Retiro"),
        ("DOMICILIO", "Envío a domicilio"),
    ]

    TRANSPORTES = [
        ("RETIRO_LOCAL", "Retiro en local"),
        ("ZEEZTON_EXPRESS", "Despacho Zeezton"),
        ("CHILEXPRESS", "Chilexpress"),
        ("STARKEN", "Starken"),
        ("BLUEXPRESS", "Blue Express"),
        ("OTRO", "Otro"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pedidos"
    )

    cliente_nombre = models.CharField(max_length=120)

    cliente_email = models.EmailField()

    cliente_telefono = models.CharField(max_length=20)

    metodo_entrega = models.CharField(
        max_length=20,
        choices=METODOS_ENTREGA,
        default="DOMICILIO"
    )

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default="PENDIENTE_PAGO"
    )

    transporte = models.CharField(
        max_length=30,
        choices=TRANSPORTES,
        blank=True,
        null=True
    )

    codigo_seguimiento = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    nota_despacho = models.TextField(
        blank=True,
        null=True
    )

    mercadopago_id = models.CharField(
    max_length=120,
    blank=True,
    null=True
    )

    estado_pago = models.CharField(
    max_length=30,
    default="pendiente"
    )
    
    stock_descontado = models.BooleanField(default=False)

    subtotal = models.PositiveIntegerField(default=0)

    costo_envio = models.PositiveIntegerField(default=0)

    total = models.PositiveIntegerField(default=0)

    creado = models.DateTimeField(auto_now_add=True)

    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def calcular_total(self):

        self.subtotal = sum(
            detalle.subtotal
            for detalle in self.detalles.all()
        )

        self.total = self.subtotal + self.costo_envio

        self.save(update_fields=[
            "subtotal",
            "total"
        ])



    @property
    def seguimiento_disponible(self):
        return bool(self.codigo_seguimiento)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre}"




class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Detalle de pedido"
        verbose_name_plural = "Detalles de pedido"

    def save(self, *args, **kwargs): 
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio

        self.subtotal = self.precio_unitario * self.cantidad

        super().save(*args, **kwargs)

        self.pedido.calcular_total()

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"









class DireccionEntrega(models.Model):
    usuario = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name="direcciones_entrega"
    )

    nombre_completo = models.CharField(max_length=120)
    telefono = models.CharField(max_length=20)
    region = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    calle = models.CharField(max_length=150)
    numero = models.CharField(max_length=30)
    referencia = models.TextField(blank=True, null=True)

    predeterminada = models.BooleanField(default=False)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.comuna}"
    



class TarifaEnvio(models.Model):
    comuna = models.CharField(max_length=100, unique=True)
    costo = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["comuna"]
        verbose_name = "Tarifa de envío"
        verbose_name_plural = "Tarifas de envío"

    def __str__(self):
        return f"{self.comuna} - ${self.costo}"