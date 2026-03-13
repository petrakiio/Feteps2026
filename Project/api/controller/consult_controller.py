from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from model.login.user import User
from model.login.doctor import Doctor


@require_GET
def consultar_usuarios(request):
    # A consulta e liberada com token de medico ou admin123.
    codigo = request.GET.get("codigo")
    if not codigo:
        return JsonResponse({"error": "Codigo ausente"}, status=400)

    # Campos expostos no JSON de resposta.
    base_fields = (
        "id",
        "name",
        "email",
        "cpf",
        "remedio",
        "horario",
        "remedios",
        "horarios",
        "data_criacao",
        "id_doctor",
    )

    if codigo == "admin123":
        # Admin ve apenas usuarios sem medico associado.
        users = User.objects.filter(Q(id_doctor__isnull=True) | Q(id_doctor=0)).values(
            *base_fields
        )
        data = list(users)
        for item in data:
            if item.get("data_criacao"):
                item["data_criacao"] = item["data_criacao"].strftime("%Y-%m-%d %H:%M:%S")
        return JsonResponse(data, safe=False, status=200)

    # Token de medico: retorna apenas pacientes daquele medico.
    try:
        doctor = Doctor.objects.get(token=codigo)
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "Token invalido"}, status=401)

    users = User.objects.filter(id_doctor=doctor.id).values(*base_fields)
    data = list(users)
    for item in data:
        if item.get("data_criacao"):
            item["data_criacao"] = item["data_criacao"].strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse(data, safe=False, status=200)
