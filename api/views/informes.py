from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from crud.models import Informe


@csrf_exempt
def crear_informe(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        titulo = data.get("titulo")
        descripcion = data.get("descripcion")
        tipo = data.get("tipo")
        prioridad = data.get("prioridad")
        estado = data.get("estado")

        if not titulo or not descripcion:
            return JsonResponse({"error": "Faltan datos"}, status=400)

        informe = Informe.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            tipo=tipo,
            prioridad=prioridad,
            estado=estado
        )

        return JsonResponse({
            "mensaje": "Informe creado correctamente",
            "id": informe.id
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listar_informes(request):
    try:
        informes = Informe.objects.all().order_by("-creado")

        data = []

        for i in informes:
            data.append({
                "id": i.id,
                "fecha": i.creado.strftime("%d-%m-%Y %H:%M") if i.creado else "",
                "tipo": i.tipo,
                "titulo": i.titulo,
                "prioridad": i.prioridad,
                "estado": i.estado,
                "descripcion": i.descripcion,
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)