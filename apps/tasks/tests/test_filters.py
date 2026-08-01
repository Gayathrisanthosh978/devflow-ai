from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         ProjectFactory, TaskFactory)
from apps.organizations.models import OrganizationRole
from apps.tasks.models import TaskStatus


def test_filter_by_status(self):

    self.authenticate()

    TaskFactory(
        project=self.project,
        status=TaskStatus.TODO,
    )

    TaskFactory(
        project=self.project,
        status=TaskStatus.DONE,
    )

    response = self.client.get(
        self.url,
        {
            "status": TaskStatus.DONE,
        },
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK,
    )

    self.assertEqual(
        len(response.data),
        1,
    )


def test_search_tasks(self):

    self.authenticate()

    TaskFactory(
        project=self.project,
        title="Fix Login",
    )

    TaskFactory(
        project=self.project,
        title="Dashboard",
    )

    response = self.client.get(
        self.url,
        {
            "search": "Login",
        },
    )

    self.assertEqual(
        len(response.data),
        1,
    )

    self.assertEqual(
        response.data[0]["title"],
        "Fix Login",
    )


def test_order_by_title(self):

    self.authenticate()

    TaskFactory(
        project=self.project,
        title="B Task",
    )

    TaskFactory(
        project=self.project,
        title="A Task",
    )

    response = self.client.get(
        self.url,
        {
            "ordering": "title",
        },
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK,
    )

    self.assertEqual(
        response.data[0]["title"],
        "A Task",
    )
