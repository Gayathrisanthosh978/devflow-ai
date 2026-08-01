from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase


class LoginAPITests(BaseAPITestCase):

    def test_login_success(self):

        url = reverse("login")

        payload = {
            "email": self.user.email,
            "password": "password123",
        }

        response = self.client.post(
            url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

        self.assertIn(
            "refresh",
            response.data,
        )

    def test_login_invalid_password(self):

        url = reverse("login")

        payload = {
            "email": self.user.email,
            "password": "wrongpassword",
        }

        response = self.client.post(
            url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_invalid_email(self):

        url = reverse("login")

        payload = {
            "email": "unknown@example.com",
            "password": "password123",
        }

        response = self.client.post(
            url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_without_password(self):

        url = reverse("login")

        payload = {
            "email": self.user.email,
        }

        response = self.client.post(
            url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "password",
            response.data,
        )
