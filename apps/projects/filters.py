import django_filters

from .models import Project


class ProjectFilter(django_filters.FilterSet):

    status = django_filters.CharFilter()

    class Meta:
        model = Project
        fields = [
            "status",
        ]
