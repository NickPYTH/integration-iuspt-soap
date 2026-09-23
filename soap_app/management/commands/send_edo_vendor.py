from django.core.management.base import BaseCommand

from soap_app.soap_client import send_edo_vendor


class Command(BaseCommand):
    help = "Отправляет тестовый пакет EDOVendorSendAsync."

    def handle(self, *args, **options):
        records = [
            {
                "INN": "7707083893",
                "KPP": "770701001",
                "FNS_ID": "0000",
                "Vendor": "VENDOR-001",
            }
        ]
        result = send_edo_vendor(records)
        self.stdout.write("transaction_id=%s success=%s" % (result["transaction_id"], result["success"]))
        self.stdout.write(str(result["external_response"]))
