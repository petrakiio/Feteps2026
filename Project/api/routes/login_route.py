from controller.login_controller import cadastro, logar
from django.views.decorators.csrf import csrf_exempt

class LoginRoutes:
    @staticmethod
    @csrf_exempt
    def cad(request):
        return cadastro(request)

    @staticmethod
    @csrf_exempt
    def login(request):
        return logar(request)
    
