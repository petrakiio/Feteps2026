from controller.instituicao_controller import (
    criar_instituicao,
    listar_instituicoes,
    detalhar_instituicao,
)


class InstituicaoRoutes:
    @staticmethod
    def cad(request):
        return criar_instituicao(request)

    @staticmethod
    def list(request):
        return listar_instituicoes(request)

    @staticmethod
    def detail(request, id_doctor):
        return detalhar_instituicao(request, id_doctor)
