from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User


class RegisterAPITests(APITestCase):

    def test_register_success(self):

        url = reverse("register")

        payload = {
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "Password@123",
            "confirm_password": "Password@123",
        }
        response = self.client.post(
            url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(User.objects.filter(email="john@example.com").exists())

    def test_register_duplicate_email(self):

        User.objects.create_user(
            email="john@example.com",
            password="Password123!",
        )

        url = reverse("register")

        payload = {
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "Password@123",
            "confirm_password": "Password@123",
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

    def test_register_without_email(self):

        url = reverse("register")

        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "password": "Password@123",
            "confirm_password": "Password@123",
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
            "email",
            response.data,
        )

    def test_register_password_mismatch(self):

        url = reverse("register")

        payload = {
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "Password@123",
            "confirm_password": "Password@456",
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
            "confirm_password",
            response.data,
        )
