from django.test import TestCase

from apps.common.tests.factories import ProjectFactory


class ProjectFactoryTests(TestCase):

    def test_create_project(self):

        project = ProjectFactory()

        self.assertTrue(project.name.startswith("Project"))

        self.assertEqual(
            project.description,
            "Test project",
        )

        self.assertIsNotNone(
            project.organization,
        )

        self.assertEqual(
            project.created_by,
            project.organization.created_by,
        )
