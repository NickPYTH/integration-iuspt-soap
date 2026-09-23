from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import SoapTransaction


@admin.register(SoapTransaction)
class SoapTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "direction", "operation", "status", "created_at", "updated_at")
    list_filter = ("direction", "status", "created_at")
    search_fields = ("id", "status")
    readonly_fields = (
        "id",
        "direction",
        "status",
        "created_at",
        "updated_at",
        "request_preview",
        "response_preview",
        "external_preview",
    )
    fields = readonly_fields
    ordering = ("-created_at",)

    @admin.display(description="Операция")
    def operation(self, obj):
        if isinstance(obj.request_data, dict):
            return obj.request_data.get("operation") or "—"
        return "—"

    def _pretty_json(self, data):
        import json

        if data in (None, "", {}):
            return "—"
        text = json.dumps(data, ensure_ascii=False, indent=2)
        return format_html("<pre style='white-space:pre-wrap;max-width:80vw;'>{}</pre>", text)

    @admin.display(description="Входящие данные")
    def request_preview(self, obj):
        return mark_safe(self._pretty_json(obj.request_data))

    @admin.display(description="Ответ")
    def response_preview(self, obj):
        return mark_safe(self._pretty_json(obj.response_data))

    @admin.display(description="Ответ внешней стороны")
    def external_preview(self, obj):
        return mark_safe(self._pretty_json(obj.external_response))
