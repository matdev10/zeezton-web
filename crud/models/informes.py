from django.db import models


# 7. INFORMES


class Informe(models.Model):
    TIPO_CHOICES = [
        ("Mejora", "Mejora"),
        ("Reclamo", "Reclamo"),
        ("Error del sistema", "Error del sistema"),
        ("Problema de stock", "Problema de stock"),
        ("Problema con cliente", "Problema con cliente"),
        ("Problema con venta", "Problema con venta"),
        ("Proveedor", "Proveedor"),
        ("Otro", "Otro"),
    ]

    PRIORIDAD_CHOICES = [
        ("Baja", "Baja"),
        ("Media", "Media"),
        ("Alta", "Alta"),
    ]

    ESTADO_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("En revisión", "En revisión"),
        ("Resuelto", "Resuelto"),
    ]

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default="Baja")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Pendiente")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.tipo} - {self.titulo}"








