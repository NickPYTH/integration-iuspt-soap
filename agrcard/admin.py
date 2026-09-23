from django.contrib import admin

from agrcard.models import AgrCard


@admin.register(AgrCard)
class AgrCardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "iuspt_card",
        "directum_card",
        "cr_ed",
        "iuspt_vendor",
        "card_date",
        "card_title",
        "created_at",
    )
    list_filter = ("cr_ed", "card_date")
    search_fields = ("iuspt_card", "directum_card", "iuspt_vendor", "hist_id", "card_title")
    readonly_fields = ("created_at", "updated_at")
