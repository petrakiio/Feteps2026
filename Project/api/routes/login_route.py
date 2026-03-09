from controller.login_controller import cadastro, logar

class LoginRoutes:
    @staticmethod
    def cad(request):
        return cadastro(request)

    @staticmethod
    def login(request):
        return logar(request)
    
