from django.urls import path

from .views import TaskActivityAPIView

urlpatterns = [
    path(
        "tasks/<uuid:task_id>/activities/",
        TaskActivityAPIView.as_view(),
        name="task-activities",
    ),
]