from rest_framework import serializers

from apps.tasks.models import Task


class DashboardTaskSerializer(serializers.ModelSerializer):

    project_name = serializers.CharField(
        source="project.name",
        read_only=True,
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "project_name",
            "status",
            "priority",
            "due_date",
        )
