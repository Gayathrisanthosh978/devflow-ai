from django.db import transaction

from .models import Notification


class NotificationService:

    @staticmethod
    @transaction.atomic
    def create_notification(
        *,
        recipient,
        actor,
        notification_type,
        message,
        task=None,
        metadata=None,
    ):

        if recipient == actor:
            return None

        return Notification.objects.create(
            recipient=recipient,
            actor=actor,
            task=task,
            notification_type=notification_type,
            message=message,
            metadata=metadata or {},
        )

    @staticmethod
    def list_notifications(*, user):

        return (
            Notification.objects.filter(
                recipient=user,
            )
            .select_related("actor")
            .order_by("-created_at")
        )


    @staticmethod
    @transaction.atomic
    def mark_as_read(*, notification):

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return notification


    @staticmethod
    @transaction.atomic
    def mark_all_as_read(*, user):

        Notification.objects.filter(
            recipient=user,
            is_read=False,
        ).update(
            is_read=True,
        )