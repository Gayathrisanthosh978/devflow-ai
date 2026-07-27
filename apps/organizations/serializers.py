from rest_framework import serializers

from .models import Organization, OrganizationMember

from apps.accounts.models import User
from .models import OrganizationRole


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "slug",
            "created_by",
            "created_at",
            "updated_at",
        )


class InviteMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()

    role = serializers.ChoiceField(
        choices=[
            (OrganizationRole.ADMIN, "Admin"),
            (OrganizationRole.PROJECT_MANAGER, "Project Manager"),
            (OrganizationRole.DEVELOPER, "Developer"),
            (OrganizationRole.CLIENT, "Client"),
            (OrganizationRole.TEAMLEAD,"TeamLead"),
            (OrganizationRole.QA,"Qa")
        ]
    )

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        return user

class OrganizationMemberSerializer(serializers.ModelSerializer):
    member_id = serializers.UUIDField(source="id", read_only=True)
    user_id = serializers.UUIDField(source="user.id", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = OrganizationMember
        fields = [
            "member_id",
            "user_id",
            "email",
            "first_name",
            "last_name",
            "role",
            "joined_at",
        ]


class UpdateMemberRoleSerializer(serializers.Serializer):

    role = serializers.ChoiceField(
    choices=[
        choice
        for choice in OrganizationRole.choices
        if choice[0] != OrganizationRole.OWNER
    ]
    )