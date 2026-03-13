import json

from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from model.login.user import User

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
    email = payload.get("email")
    password = payload.get("password")
    remedio = payload.get("remedio")
    horario = payload.get("horario")
    remedios = payload.get("remedios", [])
    horarios = payload.get("horarios", [])
    id_doctor = payload.get("id_doctor")

    # Normaliza o nome para salvar sempre em minusculo.
    if isinstance(name, str):
        name = name.strip().lower()
    if isinstance(email, str):
        email = email.strip().lower()

    # Retorna quais campos obrigatorios faltaram.
    missing = [
        field
        for field, value in {
            "nome": name,
            "email": email,
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

    # Normaliza listas quando vier um unico valor.
    if isinstance(remedios, str):
        remedios = [remedios]
    if isinstance(horarios, str):
        horarios = [horarios]

    try:
        # Persiste o novo usuario.
        user = User.objects.create(
            name=name,
            email=email,
            # Salva hash da senha, nunca texto puro.
            password=make_password(password),
            remedio=remedio,
            horario=horario,
            remedios=remedios if isinstance(remedios, list) else [],
            horarios=horarios if isinstance(horarios, list) else [],
            id_doctor=int(id_doctor) if id_doctor not in (None, "") else None,
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
    email = payload.get("email")
    password = payload.get("password")
    if isinstance(email, str):
        email = email.strip().lower()

    missing = [
        field
        for field, value in {
            "email": email,
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
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"error": "Email ou senha invalidos"}, status=401)

    # Valida hash e mantem compatibilidade com registros antigos em texto puro.
    if not check_password(password, user.password):
        if user.password != password:
            return JsonResponse({"error": "Email ou senha invalidos"}, status=401)
        user.password = make_password(password)
        user.save(update_fields=["password"])

    # Guarda o usuario autenticado na sessao.
    request.session["user_id"] = user.id
    return JsonResponse(
        {
            "message": "Login realizado",
            "user": {
                "id": user.id,
                "nome": user.name,
                "email": user.email,
            },
        },
        status=200,
    )
