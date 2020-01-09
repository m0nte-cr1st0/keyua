import factory
from factory.fuzzy import FuzzyText, FuzzyInteger

# Django imports
from django.contrib.auth import get_user_model

User = get_user_model()

USER_PASSWORD = '1234ab'
USER_EMAIL = 'juan@example.com'


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory to provide users for testing.
    """

    #: Username of the user.
    username = FuzzyText(length=12, prefix='user#')
    #: First name of the user.
    first_name = factory.Faker('first_name')
    #: Last name of the user.
    last_name = 'Doe'
    #: Email of the user.
    email = USER_EMAIL
    #: Password of the user.
    password = USER_PASSWORD

    class Meta:
        model = User


class InactiveUserFactory(UserFactory):
    #: Not active status for user.
    is_active = False