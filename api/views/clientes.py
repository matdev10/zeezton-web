from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from crud.models import Cliente


@csrf_exempt
def crear_cliente(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        cliente = Cliente.objects.create(
            numero_documento=data.get("numero_documento"),
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            fecha_nacimiento=data.get("fecha_nacimiento") or None,
            rut=data.get("rut"),
            email=data.get("email"),
            telefono=data.get("telefono"),
            direccion=data.get("direccion"),
            numero=data.get("numero"),
            comuna=data.get("comuna"),
            departamento=data.get("departamento"),
            informacion_adicional=data.get("informacion_adicional"),
        )

        return JsonResponse({
            "mensaje": "Cliente creado",
            "id": cliente.id
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def buscar_cliente_rut(request):
    try:
        rut = request.GET.get("rut")

        if not rut:
            return JsonResponse({"error": "Debe enviar un RUT"}, status=400)

        cliente = Cliente.objects.filter(rut=rut).first()

        if not cliente:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)

        return JsonResponse({
            "id": cliente.id,
            "numero_documento": cliente.numero_documento,
            "nombre": cliente.nombre or "",
            "apellido": cliente.apellido or "",
            "rut": cliente.rut or "",
            "email": cliente.email or "",
            "telefono": cliente.telefono or "",
            "direccion": cliente.direccion or "",
            "numero": cliente.numero or "",
            "comuna": cliente.comuna or "",
            "departamento": cliente.departamento or "",
            "informacion_adicional": cliente.informacion_adicional or "",
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listar_clientes(request):
    try:
        clientes = Cliente.objects.all().order_by("-id")

        data = []

        for c in clientes:
            data.append({
                "id": c.id,
                "numero_documento": c.numero_documento or "",
                "nombre": c.nombre or "",
                "apellido": c.apellido or "",
                "rut": c.rut or "",
                "email": c.email or "",
                "telefono": c.telefono or "",
                "direccion": c.direccion or "",
                "numero": c.numero or "",
                "comuna": c.comuna or "",
                "departamento": c.departamento or "",
                "informacion_adicional": c.informacion_adicional or "",
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@csrf_exempt
def eliminar_cliente(request, cliente_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        cliente = Cliente.objects.filter(id=cliente_id).first()

        if not cliente:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)

        cliente.delete()

        return JsonResponse({
            "mensaje": "Cliente eliminado correctamente"
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)