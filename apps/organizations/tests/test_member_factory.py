from django.test import TestCase

from apps.common.tests.factories import OrganizationMemberFactory


class OrganizationMemberFactoryTests(TestCase):

    def test_create_member(self):

        member = OrganizationMemberFactory()

        self.assertIsNotNone(member.organization)

        self.assertIsNotNone(member.user)
