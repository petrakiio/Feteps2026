from controller.consult_controller import consultar_usuarios

class ConsultaRoute:
    @staticmethod
    def get(request):
        # Encaminha a requisicao para o controller.
        return consultar_usuarios(request)
