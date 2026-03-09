import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from model.user import User

@csrf_exempt
@require_POST
def cadastro(request):
    payload = {}
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON invalido"}, status=400)
    else:
        payload = request.POST

    name = payload.get("nome")
    gmail = payload.get("gmail")
    password = payload.get("password")
    remedio = payload.get("remedio")
    horario = payload.get("horario")

    missing = [
        field
        for field, value in {
            "nome": name,
            "gmail": gmail,
            "password": password,
            "remedio": remedio,
            "horario": horario,
        }.items()
        if not value
    ]
    if missing:
        return JsonResponse(
            {"error": "Campos obrigatorios ausentes", "fields": missing},
            status=400,
        )

    try:
        user = User.objects.create(
            name=name,
            gmail=gmail,
            password=password,
            remedio=remedio,
            horario=horario,
        )
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse({"id": user.id, "message": "Usuario cadastrado"}, status=201)
