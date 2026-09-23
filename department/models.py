from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return f"{self.name}"


def text(value):
    if value is None:
        return ""
    return str(value).strip()


def soap_to_payload(record):
    payload = {
        "name": text(getattr(record, "Name", None))
    }
    return payload


def create_department(record):
    payload = soap_to_payload(record)
    try:
        return Department.objects.create(**payload)
    except Exception as e:
        raise ValueError("Ошибка создания подразделения") from e


def get_department(id):
    return Department.objects.filter(pk=id).first()


def list_departments():
    return Department.objects.all()


def update_department(id, record):
    obj = get_department(id)
    if obj is None:
        return None
    payload = soap_to_payload(record)
    try:
        for key, value in payload.items():
            setattr(obj, key, value)
        obj.save()
    except Exception as e:
        raise ValueError("Ошибка обновления подразделения") from e
    return obj


def delete_department(id):
    obj = get_department(id)
    if obj is None:
        return False
    obj.delete()
    return True
