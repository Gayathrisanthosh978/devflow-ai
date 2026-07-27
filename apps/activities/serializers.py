from rest_framework import serializers

from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source="user.full_name",
        read_only=True,
    )

    class Meta:
        model = ActivityLog
        fields = (
            "id",
            "action",
            "description",
            "metadata",
            "user_name",
            "created_at",
        )