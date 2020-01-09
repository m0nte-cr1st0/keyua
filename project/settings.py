import os
import djcelery

from django.utils.translation import ugettext_lazy as _l

from celery.schedules import crontab
djcelery.setup_loader()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'iy12sc%8iu2tyr27+t4*=4cir*#a_#+n)SdFPRsir$jk5kk*$7'

ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

##### Languages #####
LANGUAGES = (
    ('en', _l('English')),
    # ('ru', _l('Russian')),
)
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

INSTALLED_APPS = [
    # 'modeltranslation',

    'grappelli',
    'filebrowser',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third apps
    'compressor',
    'rest_framework',
    'rest_framework.authtoken',
    'djcelery',
    'tinymce',

    # project apps
    'project.inauth',
    'project.core',
    'project.api',
    'project.cms',
    'project.content',
    'project.mailing',
    'project.blog',
]

MIDDLEWARE = [
    # 'django.middleware.common.CommonMiddleware',
    'project.landing.middlewares.RedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'project.urls'

TEMPLATE_OPTIONS = TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'project/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                # custom processors
                'project.core.context_processors.core_context',
            ],
        }
    },
]


WSGI_APPLICATION = 'project.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # others
    'compressor.finders.CompressorFinder',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

SITE_URL = 'https://keyua.org'

AUTH_USER_MODEL = 'inauth.User'
SESSION_REFERRAL_NAME = 'invite'
# Mailing
PROJECT_EMAIL_NAME = 'KeyUa'
PROJECT_DOMAIN = 'keyua.org'

# Celery settings
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Europe/London'

# BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
BROKER_TRANSPORT = "redis"
BROKER_HOST = "127.0.0.1"  # Maps to redis host.
BROKER_PORT = 6379         # Maps to redis port.
BROKER_VHOST = "0"         # Maps to database number.

# Mandrill settings
MANDRILL_API_KEY = ''
MANDRILL_API_URL = 'https://mandrillapp.com/api/1.0/'
DEFAULT_FROM_EMAIL = ''
DEFAULT_FROM_NAME = 'KeyUa'

CELERYBEAT_SCHEDULE = {
    # Execute on the seventh day of every month.
    # Reminder about confirmation an account.
    # IMPORTANT turn CELERY_ENABLE_UTC to True, otherwise error:
    # TypeError: can't compare offset-naive and offset-aware datetimes
    'confirm_account_reminder': {
        'task': 'project.inauth.tasks.confirm_account_reminder',
        'schedule': crontab(0, 0, day_of_month='7')
    }
}

# EMAIL
DEFAULT_FROM_EMAIL = 'hello@keyua.org'
DEFAULT_TO_EMAIL = ''
DIRECTOR_EMAIL = 'boan85@gmail.com'
PROJECT_MANAGER_EMAIL = 'yana@keyua.com'
PROJECT_EMAIL = 'hello@keyua.org'
SALES_EMAIL = ''


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'keyua.feedback@gmail.com'
EMAIL_HOST_PASSWORD = '0935786917qwerty'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DIRECTOR_EMAILS_LIST = [DIRECTOR_EMAIL, PROJECT_EMAIL, PROJECT_MANAGER_EMAIL]

# TinyMCE
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace,media",
    'theme': "advanced",
    'width': '100%',
    'height': 600,
    'theme_advanced_buttons3_add' : "tablecontrols",
    'table_styles' : "Header 1=header1;Header 2=header2;Header 3=header3",
    'table_cell_styles' : "Header 1=header1;Header 2=header2;Header 3=header3;Table Cell=tableCel1",
    'table_row_styles' : "Header 1=header1;Header 2=header2;Header 3=header3;Table Row=tableRow1",
    'table_cell_limit' : 100,
    'table_row_limit' : 30,
    'table_col_limit' : 30,
    'mode': 'textarea',
    'menubar': 'insert',
    'toolbar': 'media',
    'theme_advanced_buttons1_add' : 'media'
}
TINYMCE_FILEBROWSER = True

# TINYPNG
TINYPNG_API_KEY = '4MKM0VKV2WiwoQRo7ROUyTQnS8KTKyH_'

X_FRAME_OPTIONS = 'ALLOW-FROM http://webvisor.com'

try:
    from project.local_settings import *
except:
    pass


APPEND_SLASH = False

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240