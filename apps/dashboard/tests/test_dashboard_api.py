from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         ProjectFactory, TaskFactory)
from apps.notifications.models import Notification, NotificationType
from apps.organizations.models import OrganizationRole


class DashboardAPITests(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

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

        TaskFactory(
            project=cls.project,
            created_by=cls.user,
        )

        Notification.objects.create(
            recipient=cls.user,
            actor=cls.user,
            notification_type=NotificationType.TASK_ASSIGNED,
            message="Assigned",
        )

        cls.url = reverse("dashboard")

    def test_dashboard(self):

        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["organizations"],
            1,
        )

        self.assertEqual(
            response.data["projects"],
            1,
        )

        self.assertEqual(
            response.data["tasks"],
            1,
        )

        self.assertEqual(
            response.data["unread_notifications"],
            1,
        )

    def test_dashboard_requires_authentication(self):

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
