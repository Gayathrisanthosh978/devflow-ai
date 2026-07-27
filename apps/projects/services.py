from django.db import transaction

from .models import Project
from apps.activities.models import ActivityAction
from apps.activities.services import ActivityService

class ProjectService:

    @staticmethod
    @transaction.atomic
    def create_project(*, organization, user, validated_data):

        project = Project.objects.create(
            organization=organization,
            created_by=user,
            **validated_data,
        )
        ActivityService.log_activity(
            organization=organization,
            project=project,
            user=user,
            action=ActivityAction.PROJECT_CREATED,
            description=f"{user.full_name} created project '{project.name}'",
        )

        return project

    @staticmethod
    def list_projects(*, organization):

        return Project.objects.filter(
            organization=organization
        ).select_related(
            "created_by",
            "organization",
        )

    @staticmethod
    @transaction.atomic
    def update_project(*, project,user, validated_data):

        for field, value in validated_data.items():
            setattr(project, field, value)

        project.save()
        ActivityService.log_activity(
            organization=project.organization,
            project=project,
            user=user,
            action=ActivityAction.PROJECT_UPDATED,
            description=f"{user.full_name} updated project '{project.name}'",
        )
        return project

    @staticmethod
    @transaction.atomic
    def delete_project(*, project):

        project.delete()