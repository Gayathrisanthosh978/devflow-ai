from django.utils import timezone

from apps.activities.models import ActivityLog
from apps.notifications.models import Notification
from apps.organizations.models import OrganizationMember
from apps.projects.models import Project
from apps.tasks.models import Task, TaskPriority, TaskStatus


class DashboardService:

    @staticmethod
    def get_dashboard(*, user):

        organization_ids = OrganizationMember.objects.filter(
            user=user,
        ).values_list(
            "organization_id",
            flat=True,
        )

        projects = Project.objects.filter(
            organization_id__in=organization_ids,
        )

        tasks = Task.objects.filter(
            project__organization_id__in=organization_ids,
        )

        return {
            "organizations": organization_ids.count(),
            "projects": projects.count(),
            "tasks": tasks.count(),
            "todo_tasks": tasks.filter(status=TaskStatus.TODO).count(),
            "in_progress_tasks": tasks.filter(status=TaskStatus.IN_PROGRESS).count(),
            "completed_tasks": tasks.filter(status=TaskStatus.DONE).count(),
            "unread_notifications": Notification.objects.filter(
                recipient=user,
                is_read=False,
            ).count(),
        }

    @staticmethod
    def get_recent_activities(*, user, limit=10):

        organization_ids = OrganizationMember.objects.filter(
            user=user,
        ).values_list(
            "organization_id",
            flat=True,
        )

        return (
            ActivityLog.objects.filter(
                organization_id__in=organization_ids,
            )
            .select_related(
                "user",
                "project",
                "task",
            )
            .order_by("-created_at")[:limit]
        )

    @staticmethod
    def get_my_tasks(*, user):

        return (
            Task.objects.filter(
                assigned_to__user=user,
            )
            .select_related(
                "project",
                "assigned_to__user",
                "created_by",
            )
            .order_by(
                "due_date",
                "-created_at",
            )
        )

    @staticmethod
    def get_project_dashboard(*, project):

        tasks = Task.objects.filter(
            project=project,
        )

        total_tasks = tasks.count()

        completed_tasks = tasks.filter(
            status=TaskStatus.DONE,
        ).count()

        progress = round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0

        return {
            "project": {
                "id": str(project.id),
                "name": project.name,
            },
            "summary": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "progress": progress,
                "overdue_tasks": tasks.filter(
                    due_date__lt=timezone.now().date(),
                )
                .exclude(
                    status=TaskStatus.DONE,
                )
                .count(),
            },
            "status_distribution": {
                "todo": tasks.filter(
                    status=TaskStatus.TODO,
                ).count(),
                "in_progress": tasks.filter(
                    status=TaskStatus.IN_PROGRESS,
                ).count(),
                "in_review": tasks.filter(
                    status=TaskStatus.IN_REVIEW,
                ).count(),
                "done": tasks.filter(
                    status=TaskStatus.DONE,
                ).count(),
                "blocked": tasks.filter(
                    status=TaskStatus.BLOCKED,
                ).count(),
            },
            "priority_distribution": {
                "low": tasks.filter(
                    priority=TaskPriority.LOW,
                ).count(),
                "medium": tasks.filter(
                    priority=TaskPriority.MEDIUM,
                ).count(),
                "high": tasks.filter(
                    priority=TaskPriority.HIGH,
                ).count(),
                "critical": tasks.filter(
                    priority=TaskPriority.CRITICAL,
                ).count(),
            },
        }
