from django.test import TestCase

from apps.common.tests.factories import UserFactory


class UserFactoryTests(TestCase):

    def test_create_user(self):

        user = UserFactory()

        self.assertEqual(
            user.email,
            "user0@example.com",
        )

        self.assertEqual(
            user.first_name,
            "John",
        )

        self.assertEqual(
            user.last_name,
            "Doe",
        )

        self.assertTrue(user.check_password("password123"))

        self.assertTrue(user.is_active)

        self.assertTrue(user.is_verified)
