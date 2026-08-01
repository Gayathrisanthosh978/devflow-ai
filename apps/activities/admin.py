from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = (
        "action",
        "user",
        "project",
        "task",
        "created_at",
    )

    list_filter = (
        "action",
        "created_at",
    )

    search_fields = (
        "description",
        "user__email",
        "project__name",
    )

    readonly_fields = ("created_at",)
