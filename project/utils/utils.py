# Django imports
from django.core.mail import EmailMessage
from django.conf import settings

# Project imports
from project.utils import enums

def strip_lower(value):
	"""
	Function removes spaces and make as lowercase
	"""
	return value.strip().lower() if value else value


def get_username_from_email(email=None):
    """
    Function returns username from email
    (part before @ in email text)

    :return: String of text before @ in email.
    :rtype: str
    """
    if not email:
        return email
    return email.split('@')[0]


def send_contact_us_notification(file, name: str, email: str, body: str, phone='', nda=False):
    if not phone:
        phone = ''
    title = 'New contact us request'
    message = '''
    New contact us request was sent.
    Check admin site for more details: http://keyua.com/keyua-admin/mailing/contactform/

    name: {}
    email: {}
    phone: {}
    nda: {}

    {}'''.format(name, email, str(phone), nda, body)
    try:
        msg = EmailMessage(
            title,
            message,
            settings.EMAIL_HOST_USER,
            settings.DIRECTOR_EMAILS_LIST
        )
        if file:
            msg.attach_file(file)
        msg.send(fail_silently=False)
    except Exception as e:
        print(e)
