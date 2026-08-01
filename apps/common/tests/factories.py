from datetime import timedelta

import factory
from django.utils import timezone

from apps.accounts.models import User
from apps.notifications.models import Notification, NotificationType
from apps.organizations.models import (Organization, OrganizationMember,
                                       OrganizationRole)
from apps.projects.models import Project
from apps.tasks.models import Task, TaskPriority, TaskStatus


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")

    first_name = "John"

    last_name = "Doe"

    password = factory.PostGenerationMethodCall(
        "set_password",
        "password123",
    )

    is_active = True

    is_verified = True


class OrganizationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f"Organization {n}")

    description = "Test organization"

    created_by = factory.SubFactory(UserFactory)


class OrganizationMemberFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = OrganizationMember

    organization = factory.SubFactory(OrganizationFactory)

    user = factory.SubFactory(UserFactory)

    role = OrganizationRole.DEVELOPER


class ProjectFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Project

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    created_by = factory.LazyAttribute(lambda obj: obj.organization.created_by)

    name = factory.Sequence(lambda n: f"Project {n}")

    description = "Test project"


class TaskFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Task

    project = factory.SubFactory(ProjectFactory)

    created_by = factory.LazyAttribute(lambda obj: obj.project.created_by)

    assigned_to = factory.SubFactory(
        OrganizationMemberFactory,
        organization=factory.SelfAttribute("..project.organization"),
    )

    title = factory.Sequence(lambda n: f"Task {n}")

    description = "Test task"

    status = TaskStatus.TODO

    priority = TaskPriority.MEDIUM

    due_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=7))

    estimated_hours = 8


class NotificationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Notification

    recipient = factory.SubFactory(UserFactory)
    actor = factory.SubFactory(UserFactory)
    notification_type = NotificationType.TASK_ASSIGNED
    message = factory.Sequence(lambda n: f"Notification {n}")
    is_read = False
    metadata = {}
