import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from model.user import User

def _get_payload(request):
    # Aceita tanto JSON (frontend separado) quanto form-data.
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8") or "{}"), None
        except json.JSONDecodeError:
            return None, JsonResponse({"error": "JSON invalido"}, status=400)
    return request.POST, None

@csrf_exempt
@require_POST
def cadastro(request):
    payload, error = _get_payload(request)
    if error:
        return error

    # Campos esperados para criar o usuario.
    name = payload.get("nome")
    gmail = payload.get("gmail")
    password = payload.get("password")
    remedio = payload.get("remedio")
    horario = payload.get("horario")

    # Retorna quais campos obrigatorios faltaram.
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
        # Persiste o novo usuario.
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

@csrf_exempt
@require_POST
def logar(request):
    payload, error = _get_payload(request)
    if error:
        return error

    # Credenciais usadas no login.
    gmail = payload.get("gmail")
    password = payload.get("password")

    missing = [
        field
        for field, value in {
            "gmail": gmail,
            "password": password,
        }.items()
        if not value
    ]
    if missing:
        return JsonResponse(
            {"error": "Campos obrigatorios ausentes", "fields": missing},
            status=400,
        )

    try:
        # Autenticacao simples por email e senha.
        user = User.objects.get(gmail=gmail, password=password)
    except User.DoesNotExist:
        return JsonResponse({"error": "Email ou senha invalidos"}, status=401)

    # Guarda o usuario autenticado na sessao.
    request.session["user_id"] = user.id
    return JsonResponse(
        {
            "message": "Login realizado",
            "user": {
                "id": user.id,
                "nome": user.name,
                "gmail": user.gmail,
            },
        },
        status=200,
    )
