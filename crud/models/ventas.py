from django.db import models
from .productos import Producto
from .clientes import Cliente
# 5. VENTAS


class Venta(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ("BOLETA", "Boleta"),
        ("FACTURA", "Factura"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ventas"
    )
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Venta #{self.id} - {self.tipo_documento} - {self.total}"

    def recalcular_total(self):
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save(update_fields=["total"])


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="detalles_venta")
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Venta {self.venta.id} - {self.producto.nombre} x {self.cantidad}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

