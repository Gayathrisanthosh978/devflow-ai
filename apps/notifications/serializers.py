from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    actor_name = serializers.CharField(
        source="actor.full_name",
        read_only=True,
    )

    class Meta:
        model = Notification
        fields = (
            "id",
            "notification_type",
            "message",
            "metadata",
            "is_read",
            "actor_name",
            "created_at",
        )
