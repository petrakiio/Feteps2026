import json

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from model.login.cuidador import Cuidador
from model.login.user import User


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
    # Lista cuidadores sem expor senha.
    cuidadores = Cuidador.objects.all().values(
        "id",
        "nome",
        "email",
        "cpf",
        "id_idoso",
        "data_criacao",
    )
    data = list(cuidadores)
    for item in data:
        if item.get("data_criacao"):
            item["data_criacao"] = item["data_criacao"].strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse(data, safe=False, status=200)


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

    if cuidador.get("data_criacao"):
        cuidador["data_criacao"] = cuidador["data_criacao"].strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse(cuidador, status=200)


@require_http_methods(["GET"])
def detalhar_cuidador_com_idoso(request, cuidador_id):
    # Retorna os dados do cuidador e do idoso associado.
    try:
        cuidador = Cuidador.objects.get(id=cuidador_id)
    except Cuidador.DoesNotExist:
        return JsonResponse({"error": "Cuidador nao encontrado"}, status=404)

    try:
        idoso = User.objects.values(
            "id",
            "name",
            "email",
            "cpf",
            "remedio",
            "horario",
            "data_criacao",
            "id_doctor",
        ).get(id=cuidador.id_idoso)
    except User.DoesNotExist:
        return JsonResponse({"error": "Idoso nao encontrado"}, status=404)

    cuidador_data = {
        "id": cuidador.id,
        "nome": cuidador.nome,
        "email": cuidador.email,
        "cpf": cuidador.cpf,
        "id_idoso": cuidador.id_idoso,
        "data_criacao": cuidador.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
    }
    if idoso.get("data_criacao"):
        idoso["data_criacao"] = idoso["data_criacao"].strftime("%Y-%m-%d %H:%M:%S")

    return JsonResponse({"cuidador": cuidador_data, "idoso": idoso}, status=200)
