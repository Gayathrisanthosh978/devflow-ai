from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.organizations.models import Organization


class OrganizationCreateAPITests(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("organization-create")

    def test_create_organization_success(self):

        self.authenticate()

        payload = {
            "name": "DevFlow AI",
            "description": "Project Management Platform",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Organization.objects.filter(
                name="DevFlow AI",
            ).exists()
        )

        def test_create_organization_requires_authentication(self):

            payload = {
                "name": "DevFlow AI",
            }

            response = self.client.post(
                self.url,
                payload,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )

        def test_create_organization_without_name(self):

            self.authenticate()

            response = self.client.post(
                self.url,
                {
                    "description": "Demo",
                },
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

            self.assertIn(
                "name",
                response.data,
            )
