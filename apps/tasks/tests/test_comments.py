from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         ProjectFactory, TaskFactory)
from apps.organizations.models import OrganizationRole
from apps.tasks.models import TaskComment


class TaskCommentAPITests(BaseAPITestCase):

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
            "task-comments",
            kwargs={
                "task_id": cls.task.id,
            },
        )

    def test_create_comment(self):

        self.authenticate()

        response = self.client.post(
            self.url,
            {
                "comment": "Looks good!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            TaskComment.objects.filter(
                task=self.task,
                comment="Looks good!",
            ).exists()
        )

    def test_create_empty_comment(self):

        self.authenticate()

        response = self.client.post(
            self.url,
            {
                "comment": "",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_list_comments(self):

        self.authenticate()

        TaskComment.objects.create(
            task=self.task,
            user=self.user,
            comment="First",
        )

        TaskComment.objects.create(
            task=self.task,
            user=self.user,
            comment="Second",
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

    def test_update_comment(self):

        self.authenticate()

        comment = TaskComment.objects.create(
            task=self.task,
            user=self.user,
            comment="Old",
        )

        url = reverse(
            "task-comment-detail",
            kwargs={
                "comment_id": comment.id,
            },
        )

        response = self.client.patch(
            url,
            {
                "comment": "Updated",
            },
            format="json",
        )

        comment.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            comment.comment,
            "Updated",
        )

    def test_delete_comment(self):

        self.authenticate()

        comment = TaskComment.objects.create(
            task=self.task,
            user=self.user,
            comment="Delete me",
        )

        url = reverse(
            "task-comment-detail",
            kwargs={
                "comment_id": comment.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            TaskComment.objects.filter(
                id=comment.id,
            ).exists()
        )
