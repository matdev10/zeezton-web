from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from crud.models import Suscriptor

@csrf_exempt
def guardar_suscriptor(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        email = request.POST.get("email", "").strip()
        nombre = request.POST.get("nombre", "").strip()
        marca = request.POST.get("marca", "").strip()
        modelo = request.POST.get("modelo", "").strip()

        if not email:
            return JsonResponse({"error": "Email requerido"}, status=400)

        Suscriptor.objects.create(
            email=email,
            nombre=nombre,
            marca=marca,
            modelo=modelo
        )

        return JsonResponse({"ok": True}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

