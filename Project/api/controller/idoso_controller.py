import json

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from model.login.user import User


def _get_payload(request):
    # Aceita JSON (frontend separado) ou form-data.
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8") or "{}"), None
        except json.JSONDecodeError:
            return None, JsonResponse({"error": "JSON invalido"}, status=400)
    return request.POST, None


@csrf_exempt
@require_http_methods(["POST"])
def cadastro_idoso(request):
    payload, error = _get_payload(request)
    if error:
        return error

    # Campos basicos do idoso (user sem doutor).
    name = payload.get("nome")
    email = payload.get("email")
    password = payload.get("password")
    cpf = payload.get("cpf")
    remedio = payload.get("remedio")
    horario = payload.get("horario")
    remedios = payload.get("remedios", [])
    horarios = payload.get("horarios", [])

    if isinstance(name, str):
        name = name.strip().lower()
    if isinstance(email, str):
        email = email.strip().lower()

    missing = [
        field
        for field, value in {
            "nome": name,
            "email": email,
            "password": password,
            "cpf": cpf,
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

    if isinstance(remedios, str):
        remedios = [remedios]
    if isinstance(horarios, str):
        horarios = [horarios]

    try:
        user = User.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            cpf=cpf,
            remedio=remedio,
            horario=horario,
            remedios=remedios if isinstance(remedios, list) else [],
            horarios=horarios if isinstance(horarios, list) else [],
            id_doctor=None,
        )
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse({"id": user.id, "message": "Idoso cadastrado"}, status=201)
