import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):

    status = django_filters.CharFilter(field_name="status")

    priority = django_filters.CharFilter(field_name="priority")

    assigned_to = django_filters.UUIDFilter(
        field_name="assigned_to__id",
    )

    due_before = django_filters.DateFilter(
        field_name="due_date",
        lookup_expr="lte",
    )

    due_after = django_filters.DateFilter(
        field_name="due_date",
        lookup_expr="gte",
    )

    class Meta:
        model = Task
        fields = [
            "status",
            "priority",
            "assigned_to",
        ]
