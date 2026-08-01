from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    DireccionEntrega,
    MensajeContacto,
    Producto,
    Reseña,
)


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = [
            'id',
            'descripcion',
            'marca',
            'precio',
            'stock',
            'imagen'
        ]
        labels = {
            'id': 'ID',
            'descripcion': 'Descripción',
            'marca': 'Marca',
            'precio': 'Precio Unitario',
            'stock': 'Stock',
            'imagen': 'Imagen'
        }
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'id': 'id'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'id': 'descripcion'}),
            'marca': forms.Select(attrs={'class': 'form-control', 'id': 'marca'}),
            'precio': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'id': 'precio'}),
            'stock': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'id': 'stock'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'id': 'imagen'})
        }



class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ["nombre", "email", "calificacion", "comentario"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "zf-input",
                "placeholder": "Tu nombre",
                "id": "id_nombre"
            }),
            "email": forms.EmailInput(attrs={
                "class": "zf-input",
                "placeholder": "Tu correo",
                "id": "id_email"
            }),
            "calificacion": forms.Select(attrs={
                "class": "zf-input",
                "id": "id_calificacion"
            }),
            "comentario": forms.Textarea(attrs={
                "class": "zf-input",
                "rows": 4,
                "placeholder": "Escribe tu reseña...",
                "id": "id_comentario"
            }),
        }

class MensajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto

        fields = [
            "tipo_mensaje",
            "nombre",
            "email",
            "telefono",
            "vehiculo",
            "repuesto",
            "numero_pedido",
            "calificacion",
            "comentario",
        ]

        labels = {
            "tipo_mensaje": "Tipo de mensaje",
            "nombre": "Nombre",
            "email": "Correo electrónico",
            "telefono": "Teléfono",
            "vehiculo": "Vehículo",
            "repuesto": "Repuesto solicitado",
            "numero_pedido": "Número de pedido",
            "calificacion": "Calificación",
            "comentario": "Mensaje",
        }

        widgets = {
            "tipo_mensaje": forms.Select(
                attrs={
                    "class": "zf-input",
                    "id": "id_tipo_mensaje",
                }
            ),
            "nombre": forms.TextInput(
                attrs={
                    "class": "zf-input",
                    "placeholder": "Tu nombre",
                    "id": "id_nombre",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "zf-input",
                    "placeholder": "correo@ejemplo.com",
                    "id": "id_email",
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "zf-input",
                    "placeholder": "+56 9 1234 5678",
                    "id": "id_telefono",
                }
            ),
            "vehiculo": forms.TextInput(
                attrs={
                    "class": "zf-input",
                    "placeholder": "Ejemplo: BMW 320i 2018",
                    "id": "id_vehiculo",
                }
            ),
            "repuesto": forms.TextInput(
                attrs={
                    "class": "zf-input",
                    "placeholder": "Nombre o número de la pieza",
                    "id": "id_repuesto",
                }
            ),
            "numero_pedido": forms.TextInput(
                attrs={
                    "class": "zf-input",
                    "placeholder": "Ejemplo: ZEE-1025",
                    "id": "id_numero_pedido",
                }
            ),
            "calificacion": forms.Select(
                attrs={
                    "class": "zf-input",
                    "id": "id_calificacion",
                }
            ),
            "comentario": forms.Textarea(
                attrs={
                    "class": "zf-input",
                    "rows": 6,
                    "placeholder": (
                        "Cuéntanos cómo podemos ayudarte..."
                    ),
                    "id": "id_comentario",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        tipo_mensaje = cleaned_data.get("tipo_mensaje")
        vehiculo = cleaned_data.get("vehiculo")
        repuesto = cleaned_data.get("repuesto")
        numero_pedido = cleaned_data.get("numero_pedido")
        calificacion = cleaned_data.get("calificacion")

        tipos_con_vehiculo = {
            MensajeContacto.TIPO_IMPORTACION,
            MensajeContacto.TIPO_COMPATIBILIDAD,
        }

        if tipo_mensaje in tipos_con_vehiculo:
            if not vehiculo:
                self.add_error(
                    "vehiculo",
                    "Indica el modelo y año de tu vehículo.",
                )

            if not repuesto:
                self.add_error(
                    "repuesto",
                    "Indica el producto o repuesto consultado.",
                )

        if (
            tipo_mensaje == MensajeContacto.TIPO_PEDIDO
            and not numero_pedido
        ):
            self.add_error(
                "numero_pedido",
                "Indica el número de tu pedido.",
            )

        if (
            tipo_mensaje == MensajeContacto.TIPO_CALIFICACION
            and not calificacion
        ):
            self.add_error(
                "calificacion",
                "Selecciona una calificación.",
            )

        return cleaned_data


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Correo electrónico"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]



class DireccionEntregaForm(forms.ModelForm):
    class Meta:
        model = DireccionEntrega
        fields = [
            "nombre_completo",
            "telefono",
            "region",
            "comuna",
            "calle",
            "numero",
            "referencia",
        ]