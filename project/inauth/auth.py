# Django imports
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login
)
from django.contrib.auth.password_validation import (
    validate_password,
    password_validators_help_texts,
    get_default_password_validators
)
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _l

# Project imports
from project.utils.users import create_user
from project.utils.utils import strip_lower
from project.inauth.models import PasswordResetRequest
from project.utils import notifications
from project.mailing.consts import USER_REGISTRATION
from project.mailing.tasks import apply_notification

User = get_user_model()


NO_EMAIL_ERR = 'no_email'
NO_PASSWORD_ERR = 'no_password'
DISABLED_USER_ERR = 'disabled_user'
INVALID_PASSWORD = 'invalid_password'
EMAIL_NOT_FOUND = 'email_not_found'


class AuthError(object):
    """
    Base class which holds authentication errors.
    """
    def __init__(self):
        self.errors = []

    errors_dict = {
        NO_EMAIL_ERR: (
            ('email'),
            _l('Email missing.')
        ),
        NO_PASSWORD_ERR: (
            ('password'),
            _l('Password missing.')
        ),
        DISABLED_USER_ERR: (
            ('email'),
            _l('Your account is not active, please contact with administrator.')
        ),
        EMAIL_NOT_FOUND: (
            ('email'),
            _l('Current email not found in system. Please register at first')
        ),
        INVALID_PASSWORD: (
            ('password'),
            _l('Invalid password.')
        )
    }

    def add_error(self, error_code):
        """
        Adds error to main errors list.

        :param error_code: The unique error key.
        """
        self.errors.append(
            {self.errors_dict[error_code][0]: self.errors_dict[error_code][1]})

    def add_custom_error(self, field, error_text):
        """
        Adds a custom error text to main errors list.

        :param field: The name of field.
        :param error_text: The custom error text.
        """
        # TODO: not allow override existing key
        self.errors.append({field: error_text})

    def get_errors(self):
        """
        Returns a main errors list.

        :returns: The list of errors.
        :rtype: list
        """
        return self.errors


class Auth(AuthError):
    """
    The main authentication class.
    """
    PORTAL = 'portal'
    MOBILE = 'mobile'

    REGISTRATION = 'registration'
    LOGIN = 'login'

    def __init__(self, email, password, target=PORTAL, **kwargs):
        super().__init__()
        self.email = strip_lower(email)
        self.password = password
        self.target = target
        self.kwargs = kwargs

    def get_user(self):
        """
        Returns user if exists, otherwise None.

        :returns: User instance or None.
        :rtype: :class:`project.inauth.models.User` or NoneType
        """
        return User.objects.filter(email=self.email).first()

    def is_valid(self):
        """
        Returns validation status.

        :returns: True if all validations were passed, False otherwise.
        :rtype: bool
        """
        if not self.email:
            self.add_error(NO_EMAIL_ERR)
            return False
        if not self.password:
            self.add_error(NO_PASSWORD_ERR)
            return False

        email_validator = EmailValidator()
        try:
            email_validator(self.email)
        except ValidationError as err:
            self.add_custom_error(
                'email',
                err.messages[0]
            )
            return False

        for validator in get_default_password_validators():
            try:
                validate_password(self.password, password_validators=[validator])
            except ValidationError:
                self.add_custom_error(
                    'password',
                    ', '.join(password_validators_help_texts([validator]))
                )
                return False

        user = self.get_user()
        if user:
            if not user.is_active:
                self.add_error(DISABLED_USER_ERR)
                return False
            if not user.check_password(self.password):
                self.add_error(INVALID_PASSWORD)
                return False
        return True

    def _finalize_auth(self, user, action, request):
        """
        Makes additional actions after finalize authentication.
        """
        if action == self.REGISTRATION:
            user = create_user(self.email, self.password, request, **self.kwargs)
            # Send registration letter
            apply_notification(user, USER_REGISTRATION, **{'user': user})

        user = authenticate(username=user.username, password=self.password)
        login(request, user)
        return user

    def login_or_register(self, request):
        """
        Makes login or registration action.

        :param request: The HTTP request.
        :type request: :class:`django.http.HttpRequest`
        :returns: Tuple with action type and `project.inauth.models.User` instance
        :rtype: tuple
        """
        if not self.is_valid():
            return (False, self.get_errors())

        user = self.get_user()
        action = self.LOGIN if user else self.REGISTRATION

        if self.target == self.PORTAL:
            notification_message = notifications.USER_LOGGED if action == self.LOGIN else notifications.USER_REGISTERED
            messages.success(request, notification_message)

        user = self._finalize_auth(user, action, request)
        return (action, user)


class ResetPassword(AuthError):
    """
    Base class for reset password.
    """

    def __init__(self, email, **kwargs):
        super().__init__()
        self.email = strip_lower(email)
        self.kwargs = kwargs

    def is_valid(self):
        """
        Returns validation status.

        :returns: True if all validations were passed, False otherwise.
        :rtype: bool
        """
        if not self.email:
            self.add_error(NO_EMAIL_ERR)
            return False

        email_validator = EmailValidator()
        try:
            email_validator(self.email)
        except ValidationError as err:
            self.add_custom_error(
                'email',
                err.messages[0]
            )
            return False

        if User.objects.filter(email=self.email, is_active=False).exists():
            self.add_error(DISABLED_USER_ERR)
            return False

        if not User.objects.filter(email=self.email).exists():
            self.add_error(EMAIL_NOT_FOUND)
            return False

        return True

    def apply_reset(self):
        """
        Applies reset password action.
        """
        if not self.is_valid():
            return (False, self.get_errors())

        reset_request = PasswordResetRequest.generate_request(self.email)
        return (True, reset_request)
