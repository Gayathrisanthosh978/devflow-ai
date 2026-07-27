from apps.organizations.models import OrganizationMember


def get_membership(*, organization_id, user):
    return OrganizationMember.objects.filter(
        organization_id=organization_id,
        user=user,
    ).first()


def has_role(*, organization_id, user, allowed_roles):
    membership = get_membership(
        organization_id=organization_id,
        user=user,
    )

    return bool(
        membership and membership.role in allowed_roles
    )