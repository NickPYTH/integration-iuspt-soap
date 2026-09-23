from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SoapTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("request_data", models.JSONField(verbose_name="Входящие SOAP-данные")),
                ("response_data", models.JSONField(default=dict, verbose_name="Отправленный ответ")),
                (
                    "external_response",
                    models.JSONField(blank=True, null=True, verbose_name="Ответ внешнего сервиса"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processed", "Processed"),
                            ("error", "Error"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
            ],
            options={
                "verbose_name": "SOAP-транзакция",
                "verbose_name_plural": "SOAP-транзакции",
                "ordering": ["-created_at"],
            },
        ),
    ]
