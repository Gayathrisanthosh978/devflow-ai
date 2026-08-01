from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.activities.serializers import ActivityLogSerializer
from apps.dashboard.serializers import DashboardTaskSerializer
from .services import DashboardService
from django.shortcuts import get_object_or_404
from apps.projects.models import Project


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = DashboardService.get_dashboard(
            user=request.user,
        )

        return Response(data)

class DashboardRecentActivitiesAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        activities = DashboardService.get_recent_activities(
            user=request.user,
        )

        serializer = ActivityLogSerializer(
            activities,
            many=True,
        )

        return Response(serializer.data)


class DashboardMyTasksAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        tasks = DashboardService.get_my_tasks(
            user=request.user,
        )

        serializer = DashboardTaskSerializer(
            tasks,
            many=True,
        )

        return Response(serializer.data)

class ProjectDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):

        project = get_object_or_404(
            Project,
            id=project_id,
        )

        data = DashboardService.get_project_dashboard(
            project=project,
        )

        return Response(data)