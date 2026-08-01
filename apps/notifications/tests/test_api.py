from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import NotificationFactory, UserFactory


class NotificationAPITests(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.url = reverse("notification-list")

    def test_list_notifications(self):

        self.authenticate()

        NotificationFactory(
            recipient=self.user,
        )

        NotificationFactory(
            recipient=self.user,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_notifications_require_authentication(self):

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_only_user_notifications_returned(self):

        self.authenticate()

        NotificationFactory(
            recipient=self.user,
        )

        NotificationFactory(
            recipient=UserFactory(),
        )

        response = self.client.get(self.url)

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_mark_notification_read(self):

        self.authenticate()

        notification = NotificationFactory(
            recipient=self.user,
            is_read=False,
        )

        url = reverse(
            "notification-detail",
            kwargs={
                "notification_id": notification.id,
            },
        )

        response = self.client.patch(url)

        notification.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            notification.is_read,
        )

    def test_cannot_mark_other_users_notification(self):

        self.authenticate()

        notification = NotificationFactory(
            recipient=UserFactory(),
        )

        url = reverse(
            "notification-detail",
            kwargs={
                "notification_id": notification.id,
            },
        )

        response = self.client.patch(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_mark_all_notifications_read(self):

        self.authenticate()

        NotificationFactory(
            recipient=self.user,
            is_read=False,
        )

        NotificationFactory(
            recipient=self.user,
            is_read=False,
        )

        url = reverse(
            "notification-read-all",
        )

        response = self.client.patch(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            self.user.notifications.filter(
                is_read=False,
            ).count(),
            0,
        )

    def test_mark_all_only_affects_current_user(self):

        self.authenticate()

        other_user = UserFactory()

        NotificationFactory(
            recipient=self.user,
            is_read=False,
        )

        NotificationFactory(
            recipient=other_user,
            is_read=False,
        )

        url = reverse(
            "notification-read-all",
        )

        self.client.patch(url)

        self.assertEqual(
            other_user.notifications.filter(
                is_read=False,
            ).count(),
            1,
        )
