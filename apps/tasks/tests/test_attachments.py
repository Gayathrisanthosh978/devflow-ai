from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         ProjectFactory, TaskFactory)
from apps.organizations.models import OrganizationRole
from apps.tasks.models import TaskAttachment


class TaskAttachmentAPITests(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.organization = OrganizationFactory(created_by=cls.user)

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
            "task-attachments",
            kwargs={"task_id": cls.task.id},
        )

    def test_upload_attachment(self):

        self.authenticate()

        uploaded_file = SimpleUploadedFile(
            "sample.pdf",
            b"dummy content",
            content_type="application/pdf",
        )

        response = self.client.post(
            self.url,
            {"file": uploaded_file},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            TaskAttachment.objects.count(),
            1,
        )

    def test_list_attachments(self):

        self.authenticate()

        uploaded_file = SimpleUploadedFile(
            "demo.pdf",
            b"content",
        )

        TaskAttachment.objects.create(
            task=self.task,
            uploaded_by=self.user,
            file=uploaded_file,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_delete_attachment(self):

        self.authenticate()

        uploaded_file = SimpleUploadedFile(
            "delete.pdf",
            b"content",
        )

        attachment = TaskAttachment.objects.create(
            task=self.task,
            uploaded_by=self.user,
            file=uploaded_file,
        )

        url = reverse(
            "task-attachment-detail",
            kwargs={
                "attachment_id": attachment.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            TaskAttachment.objects.filter(
                id=attachment.id,
            ).exists()
        )
