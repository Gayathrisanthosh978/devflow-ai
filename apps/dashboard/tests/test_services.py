from django.test import TestCase

from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         ProjectFactory, TaskFactory,
                                         UserFactory)
from apps.dashboard.services import DashboardService
from apps.notifications.models import Notification, NotificationType
from apps.organizations.models import OrganizationRole
from apps.tasks.models import TaskStatus


class DashboardServiceTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = UserFactory()

        cls.organization = OrganizationFactory(
            created_by=cls.user,
        )

        OrganizationMemberFactory(
            organization=cls.organization,
            user=cls.user,
            role=OrganizationRole.OWNER,
        )

        cls.project = ProjectFactory(
            organization=cls.organization,
            created_by=cls.user,
        )

    def test_empty_dashboard(self):

        data = DashboardService.get_dashboard(
            user=self.user,
        )

        self.assertEqual(
            data["organizations"],
            1,
        )

        self.assertEqual(
            data["projects"],
            1,
        )

        self.assertEqual(
            data["tasks"],
            0,
        )

        self.assertEqual(
            data["unread_notifications"],
            0,
        )

    def test_task_counts(self):

        TaskFactory(
            project=self.project,
            status=TaskStatus.TODO,
        )

        TaskFactory(
            project=self.project,
            status=TaskStatus.IN_PROGRESS,
        )

        TaskFactory(
            project=self.project,
            status=TaskStatus.DONE,
        )

        data = DashboardService.get_dashboard(
            user=self.user,
        )

        self.assertEqual(data["tasks"], 3)
        self.assertEqual(data["todo_tasks"], 1)
        self.assertEqual(data["in_progress_tasks"], 1)
        self.assertEqual(data["completed_tasks"], 1)

    def test_unread_notifications(self):

        Notification.objects.create(
            recipient=self.user,
            actor=self.user,
            notification_type=NotificationType.TASK_ASSIGNED,
            message="Assigned",
        )

        Notification.objects.create(
            recipient=self.user,
            actor=self.user,
            notification_type=NotificationType.TASK_COMMENTED,
            message="Comment",
            is_read=True,
        )

        data = DashboardService.get_dashboard(
            user=self.user,
        )

        self.assertEqual(
            data["unread_notifications"],
            1,
        )
