from django.test import TestCase

from apps.common.tests.factories import OrganizationFactory


class OrganizationFactoryTests(TestCase):

    def test_create_organization(self):

        organization = OrganizationFactory()

        self.assertTrue(organization.name.startswith("Organization"))

        self.assertEqual(
            organization.description,
            "Test organization",
        )

        self.assertIsNotNone(organization.created_by)
