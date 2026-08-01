from apps.organizations.models import OrganizationMember


def get_membership(*, user, organization_id):

    if not user.is_authenticated:
        return None

    return OrganizationMember.objects.filter(
        user=user,
        organization_id=organization_id,
    ).first()


def has_role(user, organization_id, allowed_roles):
    if not user.is_authenticated:
        return False

    membership = get_membership(
        user=user,
        organization_id=organization_id,
    )

    if membership is None:
        return False

    return membership.role in allowed_roles
