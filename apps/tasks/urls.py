from django.urls import path

from .views import (TaskAttachmentDetailAPIView,
                    TaskAttachmentListCreateAPIView, TaskCommentDetailAPIView,
                    TaskCommentListCreateAPIView, TaskDetailAPIView,
                    TaskListCreateAPIView)

urlpatterns = [
    path(
        "organizations/<uuid:organization_id>/projects/<uuid:project_id>/tasks/",
        TaskListCreateAPIView.as_view(),
        name="task-list-create",
    ),
    path(
        "tasks/<uuid:task_id>/",
        TaskDetailAPIView.as_view(),
        name="task-detail",
    ),
    path(
        "tasks/<uuid:task_id>/comments/",
        TaskCommentListCreateAPIView.as_view(),
        name="task-comments",
    ),
    path(
        "comments/<uuid:comment_id>/",
        TaskCommentDetailAPIView.as_view(),
        name="task-comment-detail",
    ),
    path(
        "tasks/<uuid:task_id>/attachments/",
        TaskAttachmentListCreateAPIView.as_view(),
        name="task-attachments",
    ),
    path(
        "attachments/<uuid:attachment_id>/",
        TaskAttachmentDetailAPIView.as_view(),
        name="task-attachment-detail",
    ),
]
