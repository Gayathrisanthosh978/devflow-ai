from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.common.pagination import DefaultPagination
from .models import Notification
from .serializers import NotificationSerializer
from .services import NotificationService


class NotificationListAPIView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get(self, request):

        notifications = NotificationService.list_notifications(
            user=request.user,
        )

        serializer = NotificationSerializer(
            notifications,
            many=True,
        )

        return Response(serializer.data)


class NotificationDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def patch(self, request, notification_id):

        notification = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.user,
        )

        notification = NotificationService.mark_as_read(
            notification=notification,
        )

        return Response(
            NotificationSerializer(notification).data
        )


class NotificationMarkAllReadAPIView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def patch(self, request):

        NotificationService.mark_all_as_read(
            user=request.user,
        )

        return Response(
            {
                "detail": "All notifications marked as read."
            }
        )