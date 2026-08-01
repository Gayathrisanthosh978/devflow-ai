from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         ProjectFactory, TaskFactory)
from apps.organizations.models import OrganizationRole
from apps.tasks.models import Task


class TaskAPITests(BaseAPITestCase):

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

        cls.project = ProjectFactory(
            organization=cls.organization,
            created_by=cls.user,
        )

        cls.list_url = reverse(
            "task-list-create",
            kwargs={
                "organization_id": cls.organization.id,
                "project_id": cls.project.id,
            },
        )

    def test_create_task_success(self):

        self.authenticate()

        payload = {
            "title": "Implement Login",
            "description": "JWT Authentication",
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
            Task.objects.filter(
                title="Implement Login",
            ).exists()
        )

    def test_create_task_requires_authentication(self):

        response = self.client.post(
            self.list_url,
            {
                "title": "Task",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_task_without_title(self):

        self.authenticate()

        response = self.client.post(
            self.list_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "title",
            response.data,
        )

    def test_get_task(self):

        self.authenticate()

        task = TaskFactory(
            project=self.project,
            created_by=self.user,
        )

        url = reverse(
            "task-detail",
            kwargs={
                "task_id": task.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            task.title,
        )

    def test_update_task(self):

        self.authenticate()

        task = TaskFactory(
            project=self.project,
            created_by=self.user,
        )

        url = reverse(
            "task-detail",
            kwargs={
                "task_id": task.id,
            },
        )

        response = self.client.patch(
            url,
            {
                "title": "Updated Task",
            },
            format="json",
        )

        task.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            task.title,
            "Updated Task",
        )

    def test_delete_task(self):

        self.authenticate()

        task = TaskFactory(
            project=self.project,
            created_by=self.user,
        )

        url = reverse(
            "task-detail",
            kwargs={
                "task_id": task.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Task.objects.filter(
                id=task.id,
            ).exists()
        )
