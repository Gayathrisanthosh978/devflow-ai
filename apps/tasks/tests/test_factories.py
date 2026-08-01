from django.test import TestCase

from apps.common.tests.factories import TaskFactory


class TaskFactoryTests(TestCase):

    def test_create_task(self):

        task = TaskFactory()

        self.assertTrue(task.title.startswith("Task"))

        self.assertEqual(
            task.status,
            "TODO",
        )

        self.assertEqual(
            task.priority,
            "MEDIUM",
        )

        self.assertEqual(
            task.project.organization,
            task.assigned_to.organization,
        )

        self.assertEqual(
            task.created_by,
            task.project.created_by,
        )
