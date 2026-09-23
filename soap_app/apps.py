from django.apps import AppConfig


class SoapAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "soap_app"
    verbose_name = "SOAP"

    def ready(self):
        from soap_app import django_compat  # noqa: F401
        from soap_app import spyne_compat  # noqa: F401
