from controller.idoso_controller import cadastro_idoso
from django.views.decorators.csrf import csrf_exempt


class IdosoRoutes:
    @staticmethod
    @csrf_exempt
    def cad(request):
        return cadastro_idoso(request)
