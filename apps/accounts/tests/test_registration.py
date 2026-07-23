from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegistrationTests(APITestCase):

    def test_user_can_register(self):
        payload = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "Password@123",
            "confirm_password": "Password@123",
        }

        response = self.client.post(
            "/api/v1/auth/register/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                email="test@example.com"
            ).exists()
        )