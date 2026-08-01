from django.urls import path

from .views import ProjectDetailAPIView, ProjectListCreateAPIView

urlpatterns = [
    path(
        "organizations/<uuid:organization_id>/projects/",
        ProjectListCreateAPIView.as_view(),
        name="project-list-create",
    ),
    path(
        "projects/<uuid:project_id>/",
        ProjectDetailAPIView.as_view(),
        name="project-detail",
    ),
]
