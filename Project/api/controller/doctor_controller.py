import json

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
    token = payload.get("token")

    missing = [
        field
        for field, value in {
            "nome": nome,
            "idade": idade,
            "token": token,
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

    try:
        doctor = Doctor.objects.create(
            nome=nome,
            idade=idade_int,
            token=token,
        )
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse({"id": doctor.id, "message": "Doctor cadastrado"}, status=201)


@require_http_methods(["GET"])
def listar_doctors(request):
    doctors = Doctor.objects.all().values("id", "nome", "idade", "token")
    return JsonResponse(list(doctors), safe=False, status=200)


@require_http_methods(["GET"])
def detalhar_doctor(request, doctor_id):
    try:
        doctor = Doctor.objects.values("id", "nome", "idade", "token").get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "Doctor nao encontrado"}, status=404)

    return JsonResponse(doctor, status=200)
