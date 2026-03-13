import json
import secrets
import string

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from model.login.doctor import Doctor


def _get_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8") or "{}"), None
        except json.JSONDecodeError:
            return None, JsonResponse({"error": "JSON invalido"}, status=400)
    return request.POST, None


@csrf_exempt
@require_http_methods(["POST"])
def criar_doctor(request):
    payload, error = _get_payload(request)
    if error:
        return error

    nome = payload.get("nome")
    idade = payload.get("idade")
    cpf = payload.get("cpf")
    password = payload.get("password")
    paciente_ids = payload.get("paciente_ids", [])

    missing = [
        field
        for field, value in {
            "nome": nome,
            "idade": idade,
            "cpf": cpf,
            "password": password,
        }.items()
        if value in (None, "")
    ]
    if missing:
        return JsonResponse(
            {"error": "Campos obrigatorios ausentes", "fields": missing},
            status=400,
        )

    try:
        idade_int = int(idade)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Idade invalida"}, status=400)

    # Gera um token numerico de 250 digitos usando secrets.
    token = "".join(secrets.choice(string.digits) for _ in range(250))

    try:
        doctor = Doctor.objects.create(
            nome=nome,
            idade=idade_int,
            cpf=cpf,
            password=make_password(password),
            token=token,
            paciente_ids=paciente_ids if isinstance(paciente_ids, list) else [],
        )
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse(
        {"id": doctor.id, "token": doctor.token, "message": "Doctor cadastrado"},
        status=201,
    )


@require_http_methods(["GET"])
def listar_doctors(request):
    # Lista sem expor senha.
    doctors = Doctor.objects.all().values(
        "id",
        "nome",
        "idade",
        "cpf",
        "token",
        "paciente_ids",
        "data_criacao",
    )
    data = list(doctors)
    for item in data:
        if item.get("data_criacao"):
            item["data_criacao"] = item["data_criacao"].strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse(data, safe=False, status=200)


@require_http_methods(["GET"])
def detalhar_doctor(request, doctor_id):
    try:
        doctor = Doctor.objects.values(
            "id",
            "nome",
            "idade",
            "cpf",
            "token",
            "paciente_ids",
            "data_criacao",
        ).get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "Doctor nao encontrado"}, status=404)

    if doctor.get("data_criacao"):
        doctor["data_criacao"] = doctor["data_criacao"].strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse(doctor, status=200)
