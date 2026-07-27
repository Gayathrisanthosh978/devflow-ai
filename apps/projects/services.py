from django.db import transaction

from .models import Project


class ProjectService:

    @staticmethod
    @transaction.atomic
    def create_project(*, organization, user, validated_data):

        project = Project.objects.create(
            organization=organization,
            created_by=user,
            **validated_data,
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
    def update_project(*, project, validated_data):

        for field, value in validated_data.items():
            setattr(project, field, value)

        project.save()

        return project

    @staticmethod
    @transaction.atomic
    def delete_project(*, project):

        project.delete()