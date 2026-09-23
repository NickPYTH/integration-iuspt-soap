from django.contrib import admin

from edovendor.models import EdoVendor


@admin.register(EdoVendor)
class EdoVendorAdmin(admin.ModelAdmin):
    list_display = ("id", "inn", "kpp", "fns_id", "vendor", "updated_at")
    search_fields = ("inn", "kpp", "fns_id", "vendor")
    readonly_fields = ("created_at", "updated_at")
