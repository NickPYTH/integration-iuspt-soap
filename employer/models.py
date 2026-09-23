from datetime import date, datetime
from django.db import IntegrityError, models

from department.models import Department

class Employer(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    inn = models.CharField(max_length=12, unique=True, verbose_name="ИНН")
    snils = models.CharField(max_length=14, blank=True, verbose_name="СНИЛС")
    position = models.CharField(max_length=120, verbose_name="Должность")
    hire_date = models.DateField(verbose_name="Дата приёма")
    phone = models.CharField(max_length=32, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return "%s %s (%s)" % (self.last_name, self.first_name, self.inn)


def parse_hire_date(value):
    """Проверка формата даты"""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        return date.fromisoformat(value[:10])
    return None


def text(value):
    if value is None:
        return ""
    return str(value).strip()


def soap_to_payload(record):
    """Конвертируем xml-record в модель"""
    hire_date = parse_hire_date(getattr(record, "HireDate", None))
    if hire_date is None:
        raise ValueError("HireDate обязателен")
    departmentType = getattr(record, "Department", None)
    if departmentType is None:
        raise ValueError("Department обязателен")
    department = Department.objects.get(id=departmentType.Id)
    payload = {
        "last_name": text(getattr(record, "LastName", None)),
        "first_name": text(getattr(record, "FirstName", None)),
        "middle_name": text(getattr(record, "MiddleName", None)),
        "inn": text(getattr(record, "Inn", None)),
        "snils": text(getattr(record, "Snils", None)),
        "position": text(getattr(record, "Position", None)),
        "department": department,
        "hire_date": hire_date,
        "phone": text(getattr(record, "Phone", None)),
        "email": text(getattr(record, "Email", None)),
    }
    for key in ("last_name", "first_name", "inn", "position", "department"):
        if not payload[key]:
            raise ValueError("%s обязателен" % key)
    return payload


def create_employer(record):
    payload = soap_to_payload(record)
    try:
        return Employer.objects.create(**payload)
    except IntegrityError as exc:
        raise ValueError("Сотрудник с ИНН %s уже существует" % payload["inn"]) from exc


def get_employer(id):
    return Employer.objects.filter(pk=id).first()


def list_employers():
    return list(Employer.objects.all())


def update_employer(id, record):
    obj = get_employer(id)
    if obj is None:
        return None
    payload = soap_to_payload(record)
    try:
        for key, value in payload.items():
            setattr(obj, key, value)
        obj.save()
    except IntegrityError as exc:
        raise ValueError("Сотрудник с ИНН %s уже существует" % payload["inn"]) from exc
    return obj


def delete_employer(id):
    obj = get_employer(id)
    if obj is None:
        return False
    obj.delete()
    return True
