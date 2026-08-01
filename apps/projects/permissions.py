from rest_framework.permissions import BasePermission

from apps.common.permissions import has_role
from apps.organizations.models import OrganizationRole

from .models import Project


class CanManageProjects(BasePermission):

    message = "You don't have permission to manage projects."

    def has_permission(self, request, view):

        organization_id = view.kwargs.get("organization_id")

        if not organization_id:
            project_id = view.kwargs.get("project_id")

            if not project_id:
                return False

            project = Project.objects.filter(id=project_id).first()

            if not project:
                return False

            organization_id = project.organization_id

        return has_role(
            organization_id=organization_id,
            user=request.user,
            allowed_roles=[
                OrganizationRole.OWNER,
                OrganizationRole.ADMIN,
                OrganizationRole.PROJECT_MANAGER,
                OrganizationRole.TEAMLEAD,
            ],
        )
