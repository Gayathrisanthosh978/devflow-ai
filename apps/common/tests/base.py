from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.tests.factories import UserFactory


class BaseAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def setUp(self):
        self.client = APIClient()

    def authenticate(self, user=None):

        user = user or self.user

        refresh = RefreshToken.for_user(user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        return user
