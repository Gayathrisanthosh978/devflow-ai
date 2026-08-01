import uuid

from django.conf import settings
from django.db import models

from apps.organizations.models import Organization
from apps.projects.models import Project
from apps.tasks.models import Task


class ActivityAction(models.TextChoices):
    PROJECT_CREATED = "PROJECT_CREATED", "Project Created"
    PROJECT_UPDATED = "PROJECT_UPDATED", "Project Updated"

    TASK_CREATED = "TASK_CREATED", "Task Created"
    TASK_UPDATED = "TASK_UPDATED", "Task Updated"
    TASK_STATUS_CHANGED = "TASK_STATUS_CHANGED", "Task Status Changed"
    TASK_ASSIGNED = "TASK_ASSIGNED", "Task Assigned"

    COMMENT_CREATED = "COMMENT_CREATED", "Comment Created"

    ATTACHMENT_UPLOADED = "ATTACHMENT_UPLOADED", "Attachment Uploaded"
    ATTACHMENT_DELETED = "ATTACHMENT_DELETED", "Attachment Deleted"


class ActivityLog(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="activities",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    action = models.CharField(
        max_length=50,
        choices=ActivityAction.choices,
    )

    description = models.TextField()

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "activity_logs"
        ordering = ["-created_at"]

    def __str__(self):
        return self.description
