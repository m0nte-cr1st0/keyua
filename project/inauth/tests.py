# Django imports
from django.test import TestCase
from django.contrib.auth import get_user_model

# Project imports
from project.inauth.auth import (
    Auth,
    AuthError,
    ResetPassword,
    NO_EMAIL_ERR,
    NO_PASSWORD_ERR,
    DISABLED_USER_ERR,
    INVALID_PASSWORD,
    EMAIL_NOT_FOUND,
)
from project.inauth.factories import (
    UserFactory,
    InactiveUserFactory,
    USER_PASSWORD,
    USER_EMAIL
)

User = get_user_model()


class AuthTests(TestCase):
    """
    The base class for tests which covering inauth django application.

    Tests:
    1. test_auth_class - Checks workable `project.inauth.auth.Auth` class.
    2. test_reset_password_class - Checks workable `project.inauth.auth.ResetPassword` class.
    """

    def setUp(self):
        super().setUp()
        self.inactive_user = InactiveUserFactory()
        self.active_user = UserFactory(email="valid_user@test.com")

    def test_auth_class(self):
        """
        Checks workable `project.inauth.auth.Auth` class.
        """
        # Empty email
        inauth = Auth(email='', password='Password1')
        self.assertEqual(inauth.is_valid(), False)
        self.assertIn('email', inauth.get_errors()[0].keys())
        self.assertEqual(inauth.get_errors()[0]['email'], Auth.errors_dict[NO_EMAIL_ERR][1])

        # Empty password
        inauth = Auth(email='test@site.com', password='')
        self.assertEqual(inauth.is_valid(), False)
        self.assertIn('password', inauth.get_errors()[0].keys())
        self.assertEqual(inauth.get_errors()[0]['password'], Auth.errors_dict[NO_PASSWORD_ERR][1])

        # Invalid password
        inauth = Auth(email='test@site.com', password='123')
        self.assertEqual(inauth.is_valid(), False)
        self.assertIn('password', inauth.get_errors()[0].keys())
        self.assertEqual(inauth.get_errors()[0]['password'], 'Your password must contain at least 6 characters.')

        # Commonly used password error
        inauth = Auth(email='test@site.com', password='123456')
        self.assertEqual(inauth.is_valid(), False)
        self.assertIn('password', inauth.get_errors()[0].keys())
        self.assertEqual(inauth.get_errors()[0]['password'], 'Your password can\'t be a commonly used password.')

        # Inactive user
        inauth = Auth(email=USER_EMAIL, password=USER_PASSWORD)
        self.assertEqual(inauth.is_valid(), False)
        self.assertIn('email', inauth.get_errors()[0].keys())
        self.assertEqual(inauth.get_errors()[0]['email'], Auth.errors_dict[DISABLED_USER_ERR][1])

        # Valid data
        inauth = Auth(email='some@test.com', password='1234df')
        self.assertEqual(inauth.is_valid(), True)

    def test_reset_password_class(self):
        """
        Checks workable `project.inauth.auth.ResetPassword` class.
        """
        # Missing email.
        reset_password = ResetPassword(email="")
        self.assertEqual(reset_password.is_valid(), False)
        self.assertIn('email', reset_password.get_errors()[0].keys())
        self.assertEqual(reset_password.get_errors()[0]['email'], Auth.errors_dict[NO_EMAIL_ERR][1])

        # Invalid email format
        reset_password = ResetPassword(email="wrong@email")
        self.assertEqual(reset_password.is_valid(), False)
        self.assertIn('email', reset_password.get_errors()[0].keys())
        self.assertEqual(reset_password.get_errors()[0]['email'], 'Enter a valid email address.')

        # User not found.
        reset_password = ResetPassword(email="wrong@email.com")
        self.assertEqual(reset_password.is_valid(), False)
        self.assertIn('email', reset_password.get_errors()[0].keys())
        self.assertEqual(reset_password.get_errors()[0]['email'], Auth.errors_dict[EMAIL_NOT_FOUND][1])

        # Inactive user
        reset_password = ResetPassword(email="valid_user@test.com")
        self.assertEqual(reset_password.is_valid(), True)
