from routes.login_route import LoginRoutes
from routes.consulta_route import ConsultaRoute


All_Routes = {
    'Login':{
        'cadastro':LoginRoutes.cad,
        'login':LoginRoutes.login,
    },
    'Consulta':{
        'usuarios':ConsultaRoute.get,
    }
}
