from controller.login_controller import cadastro
from django.http import HttpRequest

class LoginRoutes:
    @staticmethod
    def cad(request):
        return cadastro(request)
    