from django.urls import reverse
from rest_framework import status

from apps.activities.models import ActivityAction, ActivityLog
from apps.activities.services import ActivityService
from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         ProjectFactory, TaskFactory)
from apps.organizations.models import OrganizationRole


class TaskActivityAPITests(BaseAPITestCase):

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

        cls.task = TaskFactory(
            project=cls.project,
            created_by=cls.user,
        )

        cls.url = reverse(
            "task-activities",
            kwargs={
                "task_id": cls.task.id,
            },
        )

    def test_requires_authentication(self):

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_empty_activity_list(self):

        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            0,
        )

    def test_list_task_activities(self):

        self.authenticate()

        ActivityService.log_activity(
            organization=self.organization,
            project=self.project,
            task=self.task,
            user=self.user,
            action=ActivityAction.TASK_CREATED,
            description="Task created",
        )

        ActivityService.log_activity(
            organization=self.organization,
            project=self.project,
            task=self.task,
            user=self.user,
            action=ActivityAction.TASK_UPDATED,
            description="Task updated",
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_only_returns_requested_task_activities(self):

        self.authenticate()

        other_task = TaskFactory(
            project=self.project,
            created_by=self.user,
        )

        ActivityService.log_activity(
            organization=self.organization,
            project=self.project,
            task=self.task,
            user=self.user,
            action=ActivityAction.TASK_CREATED,
            description="Task One",
        )

        ActivityService.log_activity(
            organization=self.organization,
            project=self.project,
            task=other_task,
            user=self.user,
            action=ActivityAction.TASK_CREATED,
            description="Task Two",
        )

        response = self.client.get(self.url)

        self.assertEqual(
            len(response.data),
            1,
        )
