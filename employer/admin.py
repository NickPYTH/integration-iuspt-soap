from django.contrib import admin

from employer.models import Employer


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    pass