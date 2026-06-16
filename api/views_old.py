from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

from crud.models import (
    Producto,
    Cliente,
    Venta,
    DetalleVenta,
    Informe,
    Suscriptor,
)







