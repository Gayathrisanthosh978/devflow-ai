from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase


class ProfileAPITests(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("profile")

    def test_get_profile_success(self):

        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["email"],
            self.user.email,
        )

        self.assertEqual(
            response.data["first_name"],
            self.user.first_name,
        )

        self.assertEqual(
            response.data["last_name"],
            self.user.last_name,
        )

    def test_get_profile_unauthenticated(self):

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
