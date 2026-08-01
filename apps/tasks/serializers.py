import os

from django.utils import timezone
from rest_framework import serializers

from apps.organizations.models import OrganizationMember

from .models import Task, TaskAttachment, TaskComment, TaskPriority, TaskStatus

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".zip",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


class TaskCreateSerializer(serializers.ModelSerializer):

    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=OrganizationMember.objects.all(),
        required=False,
        allow_null=True,
    )

    def validate_due_date(self, value):

        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")

        return value

    def validate_estimated_hours(self, value):

        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Estimated hours must be greater than zero."
            )

        return value

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Title cannot be empty.")

        return value

    class Meta:
        model = Task

        fields = (
            "title",
            "description",
            "priority",
            "assigned_to",
            "due_date",
            "estimated_hours",
        )


class TaskSerializer(serializers.ModelSerializer):

    created_by = serializers.EmailField(
        source="created_by.email",
        read_only=True,
    )

    assigned_to = serializers.SerializerMethodField()

    class Meta:
        model = Task

        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assigned_to",
            "created_by",
            "due_date",
            "estimated_hours",
            "created_at",
        )

    def get_assigned_to(self, obj):

        if not obj.assigned_to:
            return None

        return {
            "id": str(obj.assigned_to.id),
            "email": obj.assigned_to.user.email,
            "role": obj.assigned_to.role,
        }


class TaskUpdateSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(
        choices=TaskStatus.choices,
        required=False,
    )

    priority = serializers.ChoiceField(
        choices=TaskPriority.choices,
        required=False,
    )

    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=OrganizationMember.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task

        fields = (
            "title",
            "description",
            "status",
            "priority",
            "assigned_to",
            "due_date",
            "estimated_hours",
        )


class TaskCommentCreateSerializer(serializers.Serializer):

    comment = serializers.CharField()


class TaskCommentUpdateSerializer(serializers.Serializer):

    comment = serializers.CharField()


class TaskCommentSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)

    user = serializers.SerializerMethodField()

    class Meta:
        model = TaskComment

        fields = [
            "id",
            "user",
            "comment",
            "created_at",
            "updated_at",
        ]

    def get_user(self, obj):

        return {
            "id": obj.user.id,
            "name": obj.user.full_name,
            "email": obj.user.email,
        }


class TaskAttachmentUploadSerializer(serializers.Serializer):

    file = serializers.FileField()


class TaskAttachmentSerializer(serializers.ModelSerializer):

    uploaded_by = serializers.SerializerMethodField()

    class Meta:
        model = TaskAttachment

        fields = (
            "id",
            "original_name",
            "file",
            "uploaded_by",
            "created_at",
        )

    def get_uploaded_by(self, obj):

        return {
            "id": str(obj.uploaded_by.id),
            "name": obj.uploaded_by.full_name,
            "email": obj.uploaded_by.email,
        }

    def validate_file(self, value):

        extension = os.path.splitext(value.name)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError("Unsupported file type.")

        if value.size > MAX_FILE_SIZE:
            raise serializers.ValidationError("Maximum file size is 10 MB.")

        return value
