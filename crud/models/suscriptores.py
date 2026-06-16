from django.db import models


class Suscriptor(models.Model):

    email = models.EmailField(unique=True)

    nombre = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    marca = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    modelo = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    activo = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)

    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Suscriptor"
        verbose_name_plural = "Suscriptores"

    def __str__(self):
        return self.email