from django.db import models

from soap_app.models import SoapTransaction


class EdoVendor(models.Model):
    inn = models.CharField(max_length=12, verbose_name="ИНН")
    kpp = models.CharField(max_length=9, verbose_name="КПП")
    fns_id = models.CharField(max_length=64, verbose_name="ФНС ИД")
    vendor = models.CharField(max_length=255, verbose_name="Код кредитора в ИУС П Т")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Контрагент ЭДО"
        verbose_name_plural = "Контрагенты ЭДО"

    def __str__(self):
        return f"{self.inn} - {self.vendor}"


def text(value):
    if value is None:
        return ""
    return str(value).strip()


def soap_to_payload(record):
    payload = {
        "inn": text(getattr(record, "INN", None)),
        "kpp": text(getattr(record, "KPP", None)),
        "fns_id": text(getattr(record, "FNS_ID", None)),
        "vendor": text(getattr(record, "Vendor", None))
    }
    return payload


def create_edovendor(record):
    payload = soap_to_payload(record)
    try:
        return EdoVendor.objects.create(**payload)
    except Exception as e:
        raise e
