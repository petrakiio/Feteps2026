from controller.doctor_controller import criar_doctor, listar_doctors, detalhar_doctor
from django.views.decorators.csrf import csrf_exempt


class DoctorRoutes:
    @staticmethod
    @csrf_exempt
    def cad(request):
        return criar_doctor(request)

    @staticmethod
    def list(request):
        return listar_doctors(request)

    @staticmethod
    def detail(request, doctor_id):
        return detalhar_doctor(request, doctor_id)
