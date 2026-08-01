from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         ProjectFactory, TaskFactory)
from apps.organizations.models import OrganizationRole


def test_owner_can_create_task(self):

    OrganizationMemberFactory(
        organization=self.organization,
        user=self.user,
        role=OrganizationRole.OWNER,
    )

    self.authenticate()

    response = self.client.post(
        self.list_url,
        {
            "title": "Owner Task",
        },
        format="json",
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED,
    )


def test_admin_can_create_task(self):

    OrganizationMemberFactory(
        organization=self.organization,
        user=self.user,
        role=OrganizationRole.ADMIN,
    )

    self.authenticate()

    response = self.client.post(
        self.list_url,
        {
            "title": "Admin Task",
        },
        format="json",
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED,
    )


def test_project_manager_can_create_task(self):

    OrganizationMemberFactory(
        organization=self.organization,
        user=self.user,
        role=OrganizationRole.PROJECT_MANAGER,
    )

    self.authenticate()

    response = self.client.post(
        self.list_url,
        {
            "title": "PM Task",
        },
        format="json",
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED,
    )


def test_teamlead_can_create_task(self):

    OrganizationMemberFactory(
        organization=self.organization,
        user=self.user,
        role=OrganizationRole.TEAMLEAD,
    )

    self.authenticate()

    response = self.client.post(
        self.list_url,
        {
            "title": "Lead Task",
        },
        format="json",
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED,
    )


def test_developer_can_create_task(self):

    OrganizationMemberFactory(
        organization=self.organization,
        user=self.user,
        role=OrganizationRole.DEVELOPER,
    )

    self.authenticate()

    response = self.client.post(
        self.list_url,
        {
            "title": "Developer Task",
        },
        format="json",
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED,
    )


def test_client_cannot_create_task(self):

    OrganizationMemberFactory(
        organization=self.organization,
        user=self.user,
        role=OrganizationRole.CLIENT,
    )

    self.authenticate()

    response = self.client.post(
        self.list_url,
        {
            "title": "Client Task",
        },
        format="json",
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN,
    )


def test_anonymous_user_cannot_create_task(self):

    response = self.client.post(
        self.list_url,
        {
            "title": "Anonymous",
        },
        format="json",
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_401_UNAUTHORIZED,
    )
