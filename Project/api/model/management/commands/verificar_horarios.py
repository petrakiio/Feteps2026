import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError, ProgrammingError
from django.utils import timezone

from model.user import User
from routes.alert import notificar_roda


class Command(BaseCommand):
    help = "Verifica usuários cujo horário do remédio é igual ao minuto atual."

    def add_arguments(self, parser):
        parser.add_argument(
            "--loop",
            action="store_true",
            help="Executa continuamente, verificando a cada --interval segundos.",
        )
        parser.add_argument(
            "--interval",
            type=int,
            default=60,
            help="Intervalo em segundos entre verificações quando --loop está ativo.",
        )

    def handle(self, *args, **options):
        loop = options["loop"]
        interval = max(1, options["interval"])

        if loop:
            self.stdout.write(self.style.SUCCESS("Loop iniciado. Pressione Ctrl+C para parar."))
            try:
                while True:
                    self._executar_verificacao()
                    time.sleep(interval)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("Loop finalizado pelo usuário."))
            return

        self._executar_verificacao()

    def _executar_verificacao(self):
        agora = timezone.localtime()
        hora = agora.hour
        minuto = agora.minute

        try:
            usuarios = list(
                User.objects.filter(horario__hour=hora, horario__minute=minuto)
            )
            total = len(usuarios)
        except (OperationalError, ProgrammingError):
            self.stderr.write(
                self.style.ERROR(
                    "Tabela de usuários não encontrada. Rode 'python3 manage.py makemigrations && python3 manage.py migrate'."
                )
            )
            return

        self.stdout.write(f"[{agora.strftime('%Y-%m-%d %H:%M:%S')}] usuários no horário: {total}")

        for usuario in usuarios:
            self.stdout.write(
                f"- {usuario.name} | remédio: {usuario.remedio} | horário: {usuario.horario.strftime('%H:%M')}"
            )
            ok, detalhe = notificar_roda(
                user_name=usuario.name,
                remedio=usuario.remedio,
                horario=usuario.horario.strftime("%H:%M"),
            )
            if ok:
                self.stdout.write(self.style.SUCCESS(f"  > Arduino: {detalhe}"))
            else:
                self.stdout.write(self.style.WARNING(f"  > Arduino: {detalhe}"))
