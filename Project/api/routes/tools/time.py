from django.http import JsonResponse
from django.utils import timezone

def horario_atual(request):
    agora = timezone.localtime()
    return JsonResponse({
        "hora": agora.strftime("%H:%M:%S"),
        "data": agora.strftime("%Y-%m-%d"),
    })

def verificar_horarios():
    