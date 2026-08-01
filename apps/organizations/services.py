from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.accounts.models import User

from .models import Organization, OrganizationMember, OrganizationRole


class OrganizationService:

    @staticmethod
    @transaction.atomic
    def create_organization(*, user, validated_data):

        organization = Organization.objects.create(
            created_by=user,
            **validated_data,
        )

        OrganizationMember.objects.create(
            organization=organization,
            user=user,
            role=OrganizationRole.OWNER,
        )

        return organization

    @staticmethod
    @transaction.atomic
    def invite_member(*, organization, invited_user, role):

        if OrganizationMember.objects.filter(
            organization=organization,
            user=invited_user,
        ).exists():
            raise ValidationError(
                {"email": "User is already a member of this organization."}
            )

        member = OrganizationMember.objects.create(
            organization=organization,
            user=invited_user,
            role=role,
        )

        return member

    @staticmethod
    def list_members(*, organization):
        return (
            OrganizationMember.objects.filter(
                organization=organization,
                is_active=True,
            )
            .select_related("user")
            .order_by("joined_at")
        )

    @staticmethod
    @transaction.atomic
    def update_member_role(*, member, role):

        member.role = role
        member.save(update_fields=["role"])

        return member

    @staticmethod
    @transaction.atomic
    def remove_member(*, member):

        member.delete()
