# Create your views here.
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.pagination import DefaultPagination
from apps.organizations.models import Organization

from .models import Project
from .permissions import CanManageProjects
from .serializers import (ProjectCreateSerializer, ProjectSerializer,
                          ProjectUpdateSerializer)
from .services import ProjectService


class ProjectListCreateAPIView(APIView):

    permission_classes = [CanManageProjects]
    pagination_class = DefaultPagination

    def get(self, request, organization_id):

        organization = get_object_or_404(
            Organization,
            id=organization_id,
        )

        projects = ProjectService.list_projects(
            organization=organization,
            filters=request.query_params,
        )

        serializer = ProjectSerializer(
            projects,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, organization_id):

        organization = get_object_or_404(
            Organization,
            id=organization_id,
        )

        serializer = ProjectCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        project = ProjectService.create_project(
            organization=organization,
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_201_CREATED,
        )


class ProjectDetailAPIView(APIView):

    permission_classes = [CanManageProjects]
    pagination_class = DefaultPagination

    def get(self, request, project_id):

        project = get_object_or_404(
            Project,
            id=project_id,
        )

        serializer = ProjectSerializer(project)

        return Response(serializer.data)

    def patch(self, request, project_id):

        project = get_object_or_404(
            Project,
            id=project_id,
        )

        serializer = ProjectUpdateSerializer(
            project,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        project = ProjectService.update_project(
            project=project,
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(ProjectSerializer(project).data)

    def delete(self, request, project_id):

        project = get_object_or_404(
            Project,
            id=project_id,
        )

        ProjectService.delete_project(
            project=project,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
