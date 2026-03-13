from controller.doctor_controller import criar_doctor, listar_doctors, detalhar_doctor


class DoctorRoutes:
    @staticmethod
    def cad(request):
        return criar_doctor(request)

    @staticmethod
    def list(request):
        return listar_doctors(request)

    @staticmethod
    def detail(request, doctor_id):
        return detalhar_doctor(request, doctor_id)
