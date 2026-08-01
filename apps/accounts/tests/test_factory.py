from django.test import TestCase

from apps.common.tests.factories import UserFactory


class UserFactoryTest(TestCase):

    def test_create_user(self):

        user = UserFactory()

        self.assertEqual(
            user.email,
            "user0@example.com",
        )
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")