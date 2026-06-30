from django.contrib import admin

from apps.tenants.models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tenant",
        "role",
        "is_active",
        "joined_at",
    )

    list_filter = (
        "role",
        "is_active",
        "tenant",
    )

    search_fields = (
        "user__email",
        "tenant__name",
    )

    autocomplete_fields = (
        "user",
        "tenant",
        "invited_by",
    )
