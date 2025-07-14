from django.core.management.base import BaseCommand
from leads.models import Lead
import requests
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa leads desde el formulario de Hyvolution'

    def handle(self, *args, **kwargs):
        API_URL = "https://chile.hyvolution.com/wp-json/leads/v1/get/"
        TOKEN = "D.O#40TvIS-F*c_Px;Ij61V/e6a"  # cambia por el real o toma desde settings si prefieres

        headers = {
            "Authorization": f"Bearer {TOKEN}"
        }

        try:
            response = requests.get(API_URL, headers=headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error al conectar con la API: {e}"))
            return

        nuevos = 0
        for item in data:
            envio_id = item["envio_id"]
            fecha_envio = item["fecha_envio"]
            campos = item["datos"]

            lead, creado = Lead.objects.get_or_create(
                envio_id=envio_id,
                fuente='Hyvolution',
                defaults={
                    "fecha_envio": fecha_envio,
                    "nombre": campos.get("your-name"),
                    "apellido": campos.get("your-lastname"),
                    "cargo": campos.get("your-position"),
                    "empresa": campos.get("your-company"),
                    "email": campos.get("your-email"),
                    "telefono": campos.get("tel-588"),
                    "pais": campos.get("your-country"),
                    "ip": campos.get("submit_ip"),
                }
            )
            if creado:
                nuevos += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Leads importados: {nuevos} nuevos."))
