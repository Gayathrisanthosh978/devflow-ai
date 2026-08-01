from django.test import TestCase

from apps.common.tests.factories import (OrganizationFactory, ProjectFactory,
                                         TaskFactory, UserFactory)
from apps.notifications.models import Notification, NotificationType
from apps.notifications.services import NotificationService


class NotificationServiceTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.actor = UserFactory()
        cls.recipient = UserFactory()

        cls.organization = OrganizationFactory(
            created_by=cls.actor,
        )

        cls.project = ProjectFactory(
            organization=cls.organization,
            created_by=cls.actor,
        )

        cls.task = TaskFactory(
            project=cls.project,
            created_by=cls.actor,
        )

    def test_create_notification(self):

        NotificationService.create_notification(
            recipient=self.recipient,
            actor=self.actor,
            task=self.task,
            notification_type=NotificationType.TASK_ASSIGNED,
            message="Task assigned",
        )

        self.assertEqual(
            Notification.objects.count(),
            1,
        )

    def test_notification_recipient(self):

        NotificationService.create_notification(
            recipient=self.recipient,
            actor=self.actor,
            task=self.task,
            notification_type=NotificationType.TASK_ASSIGNED,
            message="Assigned",
        )

        notification = Notification.objects.first()

        self.assertEqual(
            notification.recipient,
            self.recipient,
        )

    def test_notification_metadata(self):

        NotificationService.create_notification(
            recipient=self.recipient,
            actor=self.actor,
            task=self.task,
            notification_type=NotificationType.TASK_ASSIGNED,
            message="Assigned",
            metadata={
                "task_id": str(self.task.id),
            },
        )

        notification = Notification.objects.first()

        self.assertEqual(
            notification.metadata["task_id"],
            str(self.task.id),
        )

    def test_notification_default_is_unread(self):

        NotificationService.create_notification(
            recipient=self.recipient,
            actor=self.actor,
            task=self.task,
            notification_type=NotificationType.TASK_ASSIGNED,
            message="Assigned",
        )

        notification = Notification.objects.first()

        self.assertFalse(
            notification.is_read,
        )
