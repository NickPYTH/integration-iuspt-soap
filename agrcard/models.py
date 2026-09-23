from django.db import models


class AgrCard(models.Model):
    iuspt_card = models.CharField(max_length=255)
    directum_card = models.IntegerField()
    cr_ed = models.CharField(max_length=255)
    iuspt_card_2 = models.CharField(max_length=255)
    card_date = models.CharField(max_length=255)
    hist_id = models.CharField(max_length=255)
    vendor_card = models.CharField(max_length=255)
    card_title = models.CharField(max_length=255)
    iuspt_vendor = models.CharField(max_length=255)
    card_kurator = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        ordering = ["-updated_at"]


def text(value):
    if value is None:
        return ""
    return str(value).strip()


def soap_to_payload(record):
    payload = {
        "iuspt_card": text(getattr(record, "IUSPTCard", None)),
        "directum_card": text(getattr(record, "DirectumCard", None)),
        "cr_ed": text(getattr(record, "CR_ED", None)),
        "iuspt_card_2": text(getattr(record, "Card_Date", None)),
        "card_date": text(getattr(record, "IUSPTCard", None)),
        "hist_id": text(getattr(record, "HistID ", None)),
        "vendor_card": text(getattr(record, "VendorCard", None)),
        "card_title": text(getattr(record, "CardTitle", None)),
        "iuspt_vendor": text(getattr(record, "IUSPTVendor", None)),
        "card_kurator": text(getattr(record, "CardKurator", None))
    }
    return payload


def create_agrcard(record):
    payload = soap_to_payload(record)
    try:
        return AgrCard.objects.create(**payload)
    except Exception as e:
        raise e
