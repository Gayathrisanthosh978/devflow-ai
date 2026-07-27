from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.organizations.models import OrganizationMember

from .models import Task,TaskComment,TaskAttachment
from apps.activities.models import ActivityAction
from apps.activities.services import ActivityService



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
        ActivityService.log_activity(
            organization=task.project.organization,
            project=task.project,
            task=task,
            user=user,
            action=ActivityAction.TASK_CREATED,
            description=f"{user.full_name} created task '{task.title}'",
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
    def update_task(*, task, user, validated_data):

        assigned_to = validated_data.get("assigned_to")

        if assigned_to:

            if assigned_to.organization_id != task.project.organization_id:
                raise ValidationError(
                    {
                        "assigned_to": "Selected member does not belong to this organization."
                    }
                )
            
        old_status = task.status
        old_assignee = task.assigned_to

        for field, value in validated_data.items():
            setattr(task, field, value)

        task.save()

        ActivityService.log_activity(
            organization=task.project.organization,
            project=task.project,
            task=task,
            user=user,
            action=ActivityAction.TASK_UPDATED,
            description=f"{user.full_name} updated task '{task.title}'",
        )

        if old_status != task.status:

            ActivityService.log_activity(
                organization=task.project.organization,
                project=task.project,
                task=task,
                user=user,
                action=ActivityAction.TASK_STATUS_CHANGED,
                description=(
                    f"{user.full_name} changed "
                    f"'{task.title}' status "
                    f"from {old_status} to {task.status}"
                ),
                metadata={
                    "old_status": old_status,
                    "new_status": task.status,
                },
            )
        if old_assignee != task.assigned_to:

            new_assignee_name = (
                task.assigned_to.user.full_name
                if task.assigned_to
                else "Unassigned"
            )

            ActivityService.log_activity(
                organization=task.project.organization,
                project=task.project,
                task=task,
                user=user,
                action=ActivityAction.TASK_ASSIGNED,
                description=(
                    f"{user.full_name} assigned "
                    f"'{task.title}' to "
                    f"{new_assignee_name}"
                ),
                metadata={
                    "old_assignee": (
                        str(old_assignee.id)
                        if old_assignee else None
                    ),
                    "new_assignee": (
                        str(task.assigned_to.id)
                        if task.assigned_to else None
                    ),
                },
            )

        

        return task

    @staticmethod
    @transaction.atomic
    def delete_task(*, task):

        task.delete()


class TaskCommentService:

    @staticmethod
    @transaction.atomic
    def create_comment(*, task, user, comment):

        task_comment = TaskComment.objects.create(
            task=task,
            user=user,
            comment=comment,
        )

        ActivityService.log_activity(
            organization=task.project.organization,
            project=task.project,
            task=task,
            user=user,
            action=ActivityAction.COMMENT_CREATED,
            description=f"{user.full_name} commented on '{task.title}'",
        )

        return task_comment

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

        attachment = TaskAttachment.objects.create(
            task=task,
            uploaded_by=uploaded_by,
            file=file,
        )

        ActivityService.log_activity(
            organization=task.project.organization,
            project=task.project,
            task=task,
            user=uploaded_by,
            action=ActivityAction.ATTACHMENT_UPLOADED,
            description=(
                f"{uploaded_by.full_name} uploaded "
                f"'{attachment.original_name}'"
            ),
            metadata={
                "filename": attachment.original_name,
            },
        )

        return attachment

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

        task = attachment.task
        user = attachment.uploaded_by
        filename = attachment.original_name
        attachment.file.delete(save=False)
        attachment.delete()
        ActivityService.log_activity(
            organization=task.project.organization,
            project=task.project,
            task=task,
            user=user,
            action=ActivityAction.ATTACHMENT_DELETED,
            description=(
                f"{user.full_name} deleted "
                f"'{filename}'"
            ),
            metadata={
                "filename": filename,
            },
        )