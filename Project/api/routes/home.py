from routes.login_user import LoginRoutes
from routes.consulta_route import ConsultaRoute
from routes.doctor_route import DoctorRoutes
from routes.instituicao_route import InstituicaoRoutes
from routes.cuidador_route import CuidadorRoutes


All_Routes = {
    'Login':{
        'cadastro':LoginRoutes.cad,
        'login':LoginRoutes.login,
    },
    'Consulta':{
        'usuarios':ConsultaRoute.get,
    },
    'Doctor':{
        'cadastro':DoctorRoutes.cad,
        'lista':DoctorRoutes.list,
        'detalhe':DoctorRoutes.detail,
    },
    'Instituicao':{
        'cadastro':InstituicaoRoutes.cad,
        'lista':InstituicaoRoutes.list,
        'detalhe':InstituicaoRoutes.detail,
    },
    'Cuidador':{
        'cadastro':CuidadorRoutes.cad,
        'lista':CuidadorRoutes.list,
        'detalhe':CuidadorRoutes.detail,
    }
}
