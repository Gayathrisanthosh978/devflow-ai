from rest_framework.permissions import BasePermission

from .models import OrganizationMember, OrganizationRole


class IsOrganizationOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        organization_id = view.kwargs.get("organization_id")

        return OrganizationMember.objects.filter(
            organization_id=organization_id,
            user=request.user,
            role__in=[
                OrganizationRole.OWNER,
                OrganizationRole.ADMIN,
            ],
            is_active=True,
        ).exists()
