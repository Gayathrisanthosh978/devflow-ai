from django.test import TestCase

from apps.activities.models import ActivityAction, ActivityLog
from apps.activities.services import ActivityService
from apps.common.tests.factories import (OrganizationFactory, ProjectFactory,
                                         TaskFactory, UserFactory)


class ActivityServiceTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = UserFactory()

        cls.organization = OrganizationFactory(
            created_by=cls.user,
        )

        cls.project = ProjectFactory(
            organization=cls.organization,
            created_by=cls.user,
        )

        cls.task = TaskFactory(
            project=cls.project,
            created_by=cls.user,
        )

    def test_log_activity(self):

        ActivityService.log_activity(
            organization=self.organization,
            project=self.project,
            task=self.task,
            user=self.user,
            action=ActivityAction.TASK_CREATED,
            description="Created task",
        )

        self.assertEqual(
            ActivityLog.objects.count(),
            1,
        )

    def test_log_activity_metadata(self):

        ActivityService.log_activity(
            organization=self.organization,
            project=self.project,
            task=self.task,
            user=self.user,
            action=ActivityAction.TASK_STATUS_CHANGED,
            description="Status changed",
            metadata={
                "old": "TODO",
                "new": "DONE",
            },
        )

        activity = ActivityLog.objects.first()

        self.assertEqual(
            activity.metadata["old"],
            "TODO",
        )

        self.assertEqual(
            activity.metadata["new"],
            "DONE",
        )

    def test_activity_organization(self):

        ActivityService.log_activity(
            organization=self.organization,
            project=self.project,
            user=self.user,
            action=ActivityAction.PROJECT_CREATED,
            description="Created",
        )

        activity = ActivityLog.objects.first()

        self.assertEqual(
            activity.organization,
            self.organization,
        )

    def test_activity_project(self):

        ActivityService.log_activity(
            organization=self.organization,
            project=self.project,
            user=self.user,
            action=ActivityAction.PROJECT_UPDATED,
            description="Updated",
        )

        activity = ActivityLog.objects.first()

        self.assertEqual(
            activity.project,
            self.project,
        )

    def test_activity_task(self):

        ActivityService.log_activity(
            organization=self.organization,
            project=self.project,
            task=self.task,
            user=self.user,
            action=ActivityAction.TASK_UPDATED,
            description="Updated",
        )

        activity = ActivityLog.objects.first()

        self.assertEqual(
            activity.task,
            self.task,
        )
