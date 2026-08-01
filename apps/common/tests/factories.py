import factory

from apps.accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Sequence(
        lambda n: f"user{n}@example.com"
    )

    first_name = "John"

    last_name = "Doe"

    password = factory.PostGenerationMethodCall(
        "set_password",
        "password123",
    )