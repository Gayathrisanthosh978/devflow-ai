from django.db import transaction
from django.db.models import Q

from .models import Project
from apps.activities.models import ActivityAction
from apps.activities.services import ActivityService
from .filters import ProjectFilter


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
    def list_projects(*, organization, filters=None):

        allowed_ordering = {
            "name",
            "-name",
            "created_at",
            "-created_at",
        }

        queryset = (
            Project.objects.filter(
                organization=organization,
            )
            .select_related(
                "created_by",
                "organization",
            )
        )
        if filters:
            queryset = ProjectFilter(
                filters,
                queryset=queryset,
            ).qs
        search = filters.get("search")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        ordering = filters.get("ordering")
        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-created_at")
            
        return queryset

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