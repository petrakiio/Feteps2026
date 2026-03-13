from controller.cuidador_controller import (
    criar_cuidador,
    listar_cuidadores,
    detalhar_cuidador,
    detalhar_cuidador_com_idoso,
)
from django.views.decorators.csrf import csrf_exempt


class CuidadorRoutes:
    @staticmethod
    @csrf_exempt
    def cad(request):
        return criar_cuidador(request)

    @staticmethod
    def list(request):
        return listar_cuidadores(request)

    @staticmethod
    def detail(request, cuidador_id):
        return detalhar_cuidador(request, cuidador_id)

    @staticmethod
    def detail_with_idoso(request, cuidador_id):
        return detalhar_cuidador_com_idoso(request, cuidador_id)
