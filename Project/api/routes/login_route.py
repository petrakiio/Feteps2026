from controller.login_controller import cadastro
from django.http import HttpRequest

def cad(request):
    return cadastro(request)
