from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.common.tests.factories import (OrganizationFactory,
                                         OrganizationMemberFactory,
                                         UserFactory)
from apps.organizations.models import OrganizationMember, OrganizationRole


class OrganizationMembersAPITests(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):

        super().setUpTestData()

        cls.organization = OrganizationFactory(
            created_by=cls.user,
        )

        cls.owner = OrganizationMember.objects.create(
            organization=cls.organization,
            user=cls.user,
            role=OrganizationRole.OWNER,
        )

        cls.url = reverse(
            "organization-members",
            kwargs={
                "organization_id": cls.organization.id,
            },
        )

    def test_invite_member_success(self):

        self.authenticate()

        invited_user = UserFactory()

        payload = {
            "email": invited_user.email,
            "role": OrganizationRole.DEVELOPER,
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
            OrganizationMember.objects.filter(
                organization=self.organization,
                user=invited_user,
            ).exists()
        )

    def test_invite_unknown_user(self):

        self.authenticate()

        payload = {
            "email": "unknown@test.com",
            "role": OrganizationRole.DEVELOPER,
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invite_existing_member(self):

        self.authenticate()

        member = UserFactory()

        OrganizationMemberFactory(
            organization=self.organization,
            user=member,
        )

        payload = {
            "email": member.email,
            "role": OrganizationRole.DEVELOPER,
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_list_members(self):

        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertGreaterEqual(
            len(response.data),
            1,
        )

    def test_update_member_role(self):

        self.authenticate()

        member = OrganizationMemberFactory(
            organization=self.organization,
        )

        url = reverse(
            "organization-member-detail",
            kwargs={
                "organization_id": self.organization.id,
                "member_id": member.id,
            },
        )

        response = self.client.patch(
            url,
            {
                "role": OrganizationRole.ADMIN,
            },
            format="json",
        )

        member.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            member.role,
            OrganizationRole.ADMIN,
        )

    def test_remove_member(self):

        self.authenticate()

        member = OrganizationMemberFactory(
            organization=self.organization,
        )

        url = reverse(
            "organization-member-detail",
            kwargs={
                "organization_id": self.organization.id,
                "member_id": member.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            OrganizationMember.objects.filter(
                id=member.id,
            ).exists()
        )

    def test_cannot_remove_owner(self):

        self.authenticate()

        url = reverse(
            "organization-member-detail",
            kwargs={
                "organization_id": self.organization.id,
                "member_id": self.owner.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
