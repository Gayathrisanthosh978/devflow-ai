from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         ProjectFactory)
from apps.organizations.models import OrganizationRole
from apps.projects.models import Project


class ProjectAPITests(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.organization = OrganizationFactory(
            created_by=cls.user,
        )

        OrganizationMemberFactory(
            organization=cls.organization,
            user=cls.user,
            role=OrganizationRole.OWNER,
        )

        cls.list_url = reverse(
            "project-list-create",
            kwargs={
                "organization_id": cls.organization.id,
            },
        )

    def test_create_project_success(self):

        self.authenticate()

        payload = {
            "name": "Backend API",
            "description": "REST API",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Project.objects.filter(
                name="Backend API",
            ).exists()
        )

    def test_create_project_requires_authentication(self):

        response = self.client.post(
            self.list_url,
            {
                "name": "Backend API",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_project_invalid_name(self):

        self.authenticate()

        response = self.client.post(
            self.list_url,
            {
                "name": "A",
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

    def test_list_projects(self):

        self.authenticate()

        ProjectFactory.create_batch(
            3,
            organization=self.organization,
            created_by=self.user,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            3,
        )

    def test_retrieve_project(self):

        self.authenticate()

        project = ProjectFactory(
            organization=self.organization,
            created_by=self.user,
        )

        url = reverse(
            "project-detail",
            kwargs={
                "project_id": project.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            str(project.id),
        )

    def test_update_project(self):

        self.authenticate()

        project = ProjectFactory(
            organization=self.organization,
            created_by=self.user,
        )

        url = reverse(
            "project-detail",
            kwargs={
                "project_id": project.id,
            },
        )

        response = self.client.patch(
            url,
            {
                "name": "Updated Project",
            },
            format="json",
        )

        project.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            project.name,
            "Updated Project",
        )

    def test_delete_project(self):

        self.authenticate()

        project = ProjectFactory(
            organization=self.organization,
            created_by=self.user,
        )

        url = reverse(
            "project-detail",
            kwargs={
                "project_id": project.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Project.objects.filter(
                id=project.id,
            ).exists()
        )
