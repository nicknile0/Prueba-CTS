from django.core.management.base import BaseCommand
from Sorteo.models import Participante

class Command(BaseCommand):
    help = "Crear participantes de prueba verificados"

    def add_arguments(self, parser):
        parser.add_argument('--count', type = int, default = 50, help = "Número de participantes a crear")

    def handle(self, *args, **options):
        n = options['count']
        base_email="cuerpoMail+"
        domain = "gmail.com"

        for i in range(1, n+1):
            email = f"{base_email}{i}@{domain}"
            if not Participante.objects.filter(email = email).exists():
                user = Participante.objects.create_user(
                    email = email,
                    nombre = f"Participante {i}",
                    telefono = f"9{100000 + i}",
                    password = "test123"
                )
                user.verificado = True
                user.save()

        self.stdout.write(self.style.SUCCESS(f'{n} participantes verificados creados'))