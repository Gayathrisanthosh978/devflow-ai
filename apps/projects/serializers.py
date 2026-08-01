from rest_framework import serializers

from .models import Project, ProjectStatus


class ProjectCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project

        fields = (
            "name",
            "description",
            "start_date",
            "end_date",
        )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Project name must be at least 3 characters."
            )

        return value


class ProjectSerializer(serializers.ModelSerializer):

    created_by = serializers.EmailField(
        source="created_by.email",
        read_only=True,
    )

    class Meta:
        model = Project

        fields = (
            "id",
            "name",
            "description",
            "status",
            "created_by",
            "start_date",
            "end_date",
            "created_at",
        )


class ProjectUpdateSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(
        choices=ProjectStatus.choices,
        required=False,
    )

    class Meta:
        model = Project

        fields = (
            "name",
            "description",
            "status",
            "start_date",
            "end_date",
        )
