from django.db import transaction

from .models import ActivityLog


class ActivityService:

    @staticmethod
    @transaction.atomic
    def log_activity(
        *,
        organization,
        project,
        user,
        action,
        description,
        task=None,
        metadata=None,
    ):

        return ActivityLog.objects.create(
            organization=organization,
            project=project,
            task=task,
            user=user,
            action=action,
            description=description,
            metadata=metadata or {},
        )

    @staticmethod
    def list_task_activities(*, task):

        return (
            ActivityLog.objects.filter(task=task)
            .select_related(
                "user",
                "project",
                "task",
            )
            .order_by("-created_at", "-id")
        )
