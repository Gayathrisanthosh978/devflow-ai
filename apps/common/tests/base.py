from rest_framework.test import APITestCase

from apps.accounts.models import User


class BaseAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
        )