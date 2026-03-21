import json
import os
from datetime import datetime, time as time_cls
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from model.login.user import User


def _get_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8") or "{}"), None
        except json.JSONDecodeError:
            return None, JsonResponse({"error": "JSON invalido"}, status=400)
    return request.POST, None


def _parse_time(value):
    if isinstance(value, time_cls):
        return value
    if not value:
        return None
    if isinstance(value, str):
        value = value.strip()
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(value, fmt).time()
        except (ValueError, TypeError):
            continue
    return None


def _user_matches_hora(user, agora):
    # Campo unico legado.
    if user.horario:
        if user.horario.hour == agora.hour and user.horario.minute == agora.minute:
            return True, user.horario

    # Lista de horarios (strings).
    if isinstance(user.horarios, list):
        for horario_raw in user.horarios:
            horario = _parse_time(horario_raw)
            if horario and horario.hour == agora.hour and horario.minute == agora.minute:
                return True, horario
    return False, None


@csrf_exempt
@require_http_methods(["GET", "POST"])
def alert(request):
    # Permite filtrar por nome, mas se nao enviar retorna todos os que batem no horario.
    payload, error = _get_payload(request)
    if error:
        return error

    nome = (
        request.GET.get("nome")
        or request.GET.get("name")
        or (payload.get("nome") if payload else None)
        or (payload.get("name") if payload else None)
    )
    if isinstance(nome, str):
        nome = nome.strip().lower()

    agora = timezone.localtime()
    usuarios = User.objects.all()
    if nome:
        usuarios = usuarios.filter(name=nome)

    encontrados = []
    for usuario in usuarios:
        ok, horario_match = _user_matches_hora(usuario, agora)
        if not ok:
            continue
        encontrados.append(
            {
                "user": usuario.name,
                "remedio": usuario.remedio,
                "horario": (
                    horario_match.strftime("%H:%M:%S") if horario_match else None
                ),
                "ok": True,
            }
        )

    return JsonResponse(
        {
            "ok": bool(encontrados),
            "total": len(encontrados),
            "usuarios": encontrados,
        },
        status=200,
    )


def notificar_roda(user_name, remedio, horario):
    url = os.getenv("ARDUINO_URL", "http://192.168.0.50/girar")
    token = os.getenv("ARDUINO_TOKEN", "").strip()
    timeout = float(os.getenv("ARDUINO_TIMEOUT", "3") or 3)

    payload = json.dumps(
        {
            "user": user_name,
            "remedio": remedio,
            "horario": horario,
        }
    ).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-Token"] = token

    req = Request(url, data=payload, headers=headers, method="POST")
    try:
        with urlopen(req, timeout=timeout) as resp:
            status = resp.status
            body = resp.read().decode("utf-8") or ""
    except HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except URLError as exc:
        return False, f"Erro de conexao: {exc.reason}"
    except Exception as exc:
        return False, f"Erro inesperado: {exc}"

    if 200 <= status < 300:
        return True, body or f"OK ({status})"
    return False, body or f"HTTP {status}"
