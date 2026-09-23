from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("soap_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="soaptransaction",
            name="direction",
            field=models.CharField(
                choices=[("in", "Приём"), ("out", "Отправка")],
                default="in",
                max_length=8,
                verbose_name="Направление",
            ),
        ),
        migrations.AlterField(
            model_name="soaptransaction",
            name="request_data",
            field=models.JSONField(verbose_name="Данные запроса"),
        ),
        migrations.AlterField(
            model_name="soaptransaction",
            name="response_data",
            field=models.JSONField(default=dict, verbose_name="Ответ"),
        ),
        migrations.AlterField(
            model_name="soaptransaction",
            name="external_response",
            field=models.JSONField(blank=True, null=True, verbose_name="Ответ внешней стороны"),
        ),
    ]
