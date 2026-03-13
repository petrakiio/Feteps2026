import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from model.login.instituicao import Instituicao


def _get_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8") or "{}"), None
        except json.JSONDecodeError:
            return None, JsonResponse({"error": "JSON invalido"}, status=400)
    return request.POST, None


@csrf_exempt
@require_http_methods(["POST"])
def criar_instituicao(request):
    payload, error = _get_payload(request)
    if error:
        return error

    id_doctor = payload.get("id_doctor")
    nome = payload.get("nome")
    cnpj = payload.get("cnpj")
    bairro = payload.get("bairro")
    rua = payload.get("rua")
    cep = payload.get("cep")

    missing = [
        field
        for field, value in {
            "id_doctor": id_doctor,
            "nome": nome,
            "cnpj": cnpj,
            "bairro": bairro,
            "rua": rua,
            "cep": cep,
        }.items()
        if value in (None, "")
    ]
    if missing:
        return JsonResponse(
            {"error": "Campos obrigatorios ausentes", "fields": missing},
            status=400,
        )

    try:
        id_doctor_int = int(id_doctor)
    except (TypeError, ValueError):
        return JsonResponse({"error": "id_doctor invalido"}, status=400)

    try:
        instituicao = Instituicao.objects.create(
            id_doctor=id_doctor_int,
            nome=nome,
            cnpj=cnpj,
            bairro=bairro,
            rua=rua,
            cep=cep,
        )
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse(
        {"id_doctor": instituicao.id_doctor, "message": "Instituicao cadastrada"},
        status=201,
    )


@require_http_methods(["GET"])
def listar_instituicoes(request):
    instituicoes = Instituicao.objects.all().values(
        "id_doctor",
        "nome",
        "cnpj",
        "bairro",
        "rua",
        "cep",
    )
    return JsonResponse(list(instituicoes), safe=False, status=200)


@require_http_methods(["GET"])
def detalhar_instituicao(request, id_doctor):
    try:
        instituicao = Instituicao.objects.values(
            "id_doctor",
            "nome",
            "cnpj",
            "bairro",
            "rua",
            "cep",
        ).get(id_doctor=id_doctor)
    except Instituicao.DoesNotExist:
        return JsonResponse({"error": "Instituicao nao encontrada"}, status=404)

    return JsonResponse(instituicao, status=200)
