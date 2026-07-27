from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404

from apps.common.permissions import get_membership, has_role
from apps.organizations.models import OrganizationRole
from apps.projects.models import Project

from .models import Task, TaskAttachment, TaskComment


class CanManageTasks(BasePermission):

    message = "You don't have permission to manage tasks."

    def has_permission(self, request, view):

        organization_id = view.kwargs.get("organization_id")

        # Create/List tasks
        if organization_id:

            project_id = view.kwargs.get("project_id")

            project = Project.objects.filter(
                id=project_id,
                organization_id=organization_id,
            ).first()

            if not project:
                return False

            organization_id = project.organization_id

        else:

            task_id = view.kwargs.get("task_id")

            if task_id:

                task = (
                    Task.objects.select_related("project")
                    .filter(id=task_id)
                    .first()
                )

                if not task:
                    return False

                organization_id = task.project.organization_id

            else:

                comment_id = view.kwargs.get("comment_id")
                if comment_id:
                    if not comment_id:
                        return False

                    comment = (
                        TaskComment.objects.select_related("task__project")
                        .filter(id=comment_id)
                        .first()
                    )

                    if not comment:
                        return False

                    organization_id = comment.task.project.organization_id

                else:

                    attachment_id = view.kwargs.get("attachment_id")

                    if not attachment_id:
                        return False

                    attachment = (
                        TaskAttachment.objects.select_related("task__project")
                        .filter(id=attachment_id)
                        .first()
                    )

                    if not attachment:
                        return False

                    organization_id = attachment.task.project.organization_id
        return has_role(
            organization_id=organization_id,
            user=request.user,
            allowed_roles=[
                OrganizationRole.OWNER,
                OrganizationRole.ADMIN,
                OrganizationRole.PROJECT_MANAGER,
                OrganizationRole.TEAMLEAD,
                OrganizationRole.DEVELOPER,
            ],
        )


class CanManageTaskComments(BasePermission):

    message = "You don't have permission to manage this comment."

    def has_permission(self, request, view):

        comment_id = view.kwargs.get("comment_id")

        comment = get_object_or_404(
            TaskComment.objects.select_related("task__project"),
            id=comment_id,
        )

        membership = get_membership(
            organization_id=comment.task.project.organization_id,
            user=request.user,
        )

        if not membership:
            return False

        # Author can edit/delete own comment
        if comment.user == request.user:
            return True

        # Managers can edit/delete any comment
        return membership.role in [
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
            OrganizationRole.PROJECT_MANAGER,
            OrganizationRole.TEAMLEAD,
        ]