from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.pagination import DefaultPagination
from apps.tasks.models import Task
from apps.tasks.permissions import CanManageTasks

from .serializers import ActivityLogSerializer
from .services import ActivityService


class TaskActivityAPIView(APIView):

    permission_classes = [CanManageTasks]
    pagination_class = DefaultPagination

    def get(self, request, task_id):

        task = get_object_or_404(
            Task,
            id=task_id,
        )

        activities = ActivityService.list_task_activities(
            task=task,
        )

        serializer = ActivityLogSerializer(
            activities,
            many=True,
        )

        return Response(serializer.data)
