# Django imports
from django.conf import settings
from django.utils.translation import ugettext as _

DEFAULT_FROM_NAME = settings.PROJECT_EMAIL_NAME
DEFAULT_FROM_EMAIL = settings.PROJECT_EMAIL

#
# Inauth app
#

#: Email about user success registration.
USER_REGISTRATION = 1
#: Email with link for resetting password.
PASSWORD_RESET = 2
#: Email with notification about success password resetting.
PASSWORD_RESET_SUCCESS = 3
#: Email with notification about confirmation the account.
ACCOUNT_CONFIRMATION = 10


EVENT_LIST = (
    (USER_REGISTRATION, "User registration"),
    (PASSWORD_RESET, "Resetting password request"),
    (PASSWORD_RESET_SUCCESS, "Password reset success"),
    (ACCOUNT_CONFIRMATION, "Account confirmation"),
)


EVENT_SUBJECTS = {
    USER_REGISTRATION: _("{site_domain}: Congratulations, you have registered!".format(site_domain=settings.PROJECT_DOMAIN)),
    PASSWORD_RESET: _("{site_domain}: Password reset request.".format(site_domain=settings.PROJECT_DOMAIN)),
    PASSWORD_RESET_SUCCESS: _("{site_domain}: You have reseted password successful.".format(site_domain=settings.PROJECT_DOMAIN)),
    ACCOUNT_CONFIRMATION: _("{site_domain}: Please confirm your email.".format(site_domain=settings.PROJECT_DOMAIN)),
}


EVENT_SETTINGS = {
    USER_REGISTRATION: {
        'FROM_NAME': DEFAULT_FROM_NAME,
        'FROM_EMAIL': DEFAULT_FROM_EMAIL,
        'SUBJECT': EVENT_SUBJECTS.get(USER_REGISTRATION),
        'TEMPLATE': 'inauth/emails/user-registration.html'
    },
    PASSWORD_RESET: {
        'FROM_NAME': DEFAULT_FROM_NAME,
        'FROM_EMAIL': DEFAULT_FROM_EMAIL,
        'SUBJECT': EVENT_SUBJECTS.get(PASSWORD_RESET),
        'TEMPLATE': 'inauth/emails/password-reset.html'
    },
    PASSWORD_RESET_SUCCESS: {
        'FROM_NAME': DEFAULT_FROM_NAME,
        'FROM_EMAIL': DEFAULT_FROM_EMAIL,
        'SUBJECT': EVENT_SUBJECTS.get(PASSWORD_RESET_SUCCESS),
        'TEMPLATE': 'inauth/emails/password-reset-done.html'
    },
    ACCOUNT_CONFIRMATION: {
        'FROM_NAME': DEFAULT_FROM_NAME,
        'FROM_EMAIL': DEFAULT_FROM_EMAIL,
        'SUBJECT': EVENT_SUBJECTS.get(ACCOUNT_CONFIRMATION),
        'TEMPLATE': 'inauth/emails/account-confirmation.html'  
    },
}

MESSAGE_NOTIFICATION_SETTINGS = {
    USER_REGISTRATION: {
        'TEXT': 'Congratulations with the registration!😀'
    },
    ACCOUNT_CONFIRMATION: {
        'TEXT': 'Please, confirm your email. We have sent you a letter with the link🙂'
    }
}