from django.urls import path

from .views import (DashboardAPIView, DashboardMyTasksAPIView,
                    DashboardRecentActivitiesAPIView, ProjectDashboardAPIView)

urlpatterns = [
    path(
        "",
        DashboardAPIView.as_view(),
        name="dashboard",
    ),
    path(
        "recent-activities/",
        DashboardRecentActivitiesAPIView.as_view(),
        name="dashboard-recent-activities",
    ),
    path(
        "my-tasks/",
        DashboardMyTasksAPIView.as_view(),
        name="dashboard-my-tasks",
    ),
    path(
        "projects/<uuid:project_id>/",
        ProjectDashboardAPIView.as_view(),
        name="project-dashboard",
    ),
]
