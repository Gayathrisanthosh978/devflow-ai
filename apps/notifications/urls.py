from django.urls import path

from .views import (
    NotificationListAPIView,
    NotificationDetailAPIView,
    NotificationMarkAllReadAPIView,
)

urlpatterns = [
    path(
        "",
        NotificationListAPIView.as_view(),
        name="notification-list",
    ),
    path(
        "read-all/",
        NotificationMarkAllReadAPIView.as_view(),
        name="notification-read-all",
    ),
    path(
        "<uuid:notification_id>/",
        NotificationDetailAPIView.as_view(),
        name="notification-detail",
    ),
]