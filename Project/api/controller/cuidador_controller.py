import json

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from model.login.cuidador import Cuidador


def _get_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8") or "{}"), None
        except json.JSONDecodeError:
            return None, JsonResponse({"error": "JSON invalido"}, status=400)
    return request.POST, None


@csrf_exempt
@require_http_methods(["POST"])
def criar_cuidador(request):
    payload, error = _get_payload(request)
    if error:
        return error

    nome = payload.get("nome")
    email = payload.get("email")
    password = payload.get("password")
    cpf = payload.get("cpf")
    id_idoso = payload.get("id_idoso")

    missing = [
        field
        for field, value in {
            "nome": nome,
            "email": email,
            "password": password,
            "cpf": cpf,
            "id_idoso": id_idoso,
        }.items()
        if value in (None, "")
    ]
    if missing:
        return JsonResponse(
            {"error": "Campos obrigatorios ausentes", "fields": missing},
            status=400,
        )

    try:
        id_idoso_int = int(id_idoso)
    except (TypeError, ValueError):
        return JsonResponse({"error": "id_idoso invalido"}, status=400)

    try:
        cuidador = Cuidador.objects.create(
            nome=nome,
            email=email,
            password=make_password(password),
            cpf=cpf,
            id_idoso=id_idoso_int,
        )
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse({"id": cuidador.id, "message": "Cuidador cadastrado"}, status=201)


@require_http_methods(["GET"])
def listar_cuidadores(request):
    cuidadores = Cuidador.objects.all().values(
        "id",
        "nome",
        "email",
        "cpf",
        "id_idoso",
        "data_criacao",
    )
    return JsonResponse(list(cuidadores), safe=False, status=200)


@require_http_methods(["GET"])
def detalhar_cuidador(request, cuidador_id):
    try:
        cuidador = Cuidador.objects.values(
            "id",
            "nome",
            "email",
            "cpf",
            "id_idoso",
            "data_criacao",
        ).get(id=cuidador_id)
    except Cuidador.DoesNotExist:
        return JsonResponse({"error": "Cuidador nao encontrado"}, status=404)

    return JsonResponse(cuidador, status=200)
