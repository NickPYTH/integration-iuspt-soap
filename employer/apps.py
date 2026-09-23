from django.apps import AppConfig


class EmployerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employer'
    verbose_name = "Сотрудники"

    def ready(self):
        from soap_app import django_compat  # noqa: F401 иначе Spyne на Python 3.14 не встанет
        from soap_app import spyne_compat  # noqa: F401
