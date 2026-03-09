from django.http import JsonResponse
from django.views.decorators.http import require_GET
from model.user import User


@require_GET
def consultar_usuarios(request):
    # A consulta so e liberada com o codigo administrativo.
    codigo = request.GET.get("codigo")
    if codigo != "admin123":
        # Sem codigo valido, nao retorna dados de usuarios.
        return JsonResponse([], safe=False, status=200)

    # Campos expostos no JSON de resposta.
    users = User.objects.all().values(
        "id",
        "name",
        "gmail",
        "remedio",
        "horario",
        "data_criacao",
    )
    return JsonResponse(list(users), safe=False, status=200)
