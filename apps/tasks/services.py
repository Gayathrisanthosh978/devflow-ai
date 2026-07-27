from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.organizations.models import OrganizationMember

from .models import Task,TaskComment,TaskAttachment



class TaskService:

    @staticmethod
    @transaction.atomic
    def create_task(*, project, user, validated_data):

        assigned_to = validated_data.get("assigned_to")

        if assigned_to:

            if assigned_to.organization_id != project.organization_id:
                raise ValidationError(
                    {
                        "assigned_to": "Selected member does not belong to this organization."
                    }
                )

        task = Task.objects.create(
            project=project,
            created_by=user,
            **validated_data,
        )

        return task

    @staticmethod
    def list_tasks(*, project):

        return (
            Task.objects.filter(project=project)
            .select_related(
                "assigned_to",
                "created_by",
                "project",
            )
        )

    @staticmethod
    @transaction.atomic
    def update_task(*, task, validated_data):

        assigned_to = validated_data.get("assigned_to")

        if assigned_to:

            if assigned_to.organization_id != task.project.organization_id:
                raise ValidationError(
                    {
                        "assigned_to": "Selected member does not belong to this organization."
                    }
                )

        for field, value in validated_data.items():
            setattr(task, field, value)

        task.save()

        return task

    @staticmethod
    @transaction.atomic
    def delete_task(*, task):

        task.delete()


class TaskCommentService:

    @staticmethod
    @transaction.atomic
    def create_comment(*, task, user, comment):

        return TaskComment.objects.create(
            task=task,
            user=user,
            comment=comment,
        )

    @staticmethod
    def list_comments(*, task):

        return (
            TaskComment.objects.filter(task=task)
            .select_related("user")
            .order_by("created_at")
        )

    @staticmethod
    @transaction.atomic
    def update_comment(*, task_comment, comment):

        task_comment.comment = comment
        task_comment.save(update_fields=["comment", "updated_at"])

        return task_comment

    @staticmethod
    @transaction.atomic
    def delete_comment(*, task_comment):

        task_comment.delete()


class TaskAttachmentService:

    @staticmethod
    @transaction.atomic
    def upload_attachment(*, task, uploaded_by, file):

        return TaskAttachment.objects.create(
            task=task,
            uploaded_by=uploaded_by,
            file=file,
        )

    @staticmethod
    def list_attachments(*, task):

        return (
            TaskAttachment.objects.filter(task=task)
            .select_related("uploaded_by")
            .order_by("created_at")
        )

    @staticmethod
    @transaction.atomic
    def delete_attachment(*, attachment):

        attachment.delete()