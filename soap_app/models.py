from django.db import models


class SoapTransaction(models.Model):
    DIRECTION_IN = "in"
    DIRECTION_OUT = "out"
    DIRECTION_CHOICES = [
        (DIRECTION_IN, "Приём"),
        (DIRECTION_OUT, "Отправка"),
    ]

    STATUS_PENDING = "pending"
    STATUS_PROCESSED = "processed"
    STATUS_ERROR = "error"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSED, "Processed"),
        (STATUS_ERROR, "Error"),
    ]

    direction = models.CharField(
        max_length=8,
        choices=DIRECTION_CHOICES,
        default=DIRECTION_IN,
        verbose_name="Направление",
    )
    request_data = models.JSONField(verbose_name="Данные запроса", default=dict)
    response_data = models.JSONField(verbose_name="Ответ", default=dict)
    external_response = models.JSONField(
        verbose_name="Ответ внешней стороны",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "SOAP-транзакция"
        verbose_name_plural = "SOAP-транзакции"

    def __str__(self):
        return "SoapTransaction #%s (%s)" % (self.pk, self.status)
