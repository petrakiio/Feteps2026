from controller.instituicao_controller import (
    criar_instituicao,
    listar_instituicoes,
    detalhar_instituicao,
)
from django.views.decorators.csrf import csrf_exempt


class InstituicaoRoutes:
    @staticmethod
    @csrf_exempt
    def cad(request):
        return criar_instituicao(request)

    @staticmethod
    def list(request):
        return listar_instituicoes(request)

    @staticmethod
    def detail(request, id_doctor):
        return detalhar_instituicao(request, id_doctor)
