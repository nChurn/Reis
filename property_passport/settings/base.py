# import os
# import logging, logging.config
# import sys
# from django.utils.log import DEFAULT_LOGGING
#
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
import socket
import os
import sys
from django.contrib.messages import constants as messages

BASE_DIR =  os.path.dirname(os.path.dirname(__file__)) #os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Application definition

INSTALLED_APPS = [
    'passport_app.apps.PassportAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'django_render_partial',    
    'bootstrap4',
    'rest_framework',
    'django_extensions',
    'background_task',
    'django_crontab',
    'fontawesome',
    'jquery',
    'captcha',
    'crispy_forms',
    'django_select2',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CRONJOBS = [
    # ('*/5 * * * *', 'passport_app.cron.my_scheduled_job')
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'property_passport.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'property_passport.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# MESSAGE_TAGS = {
#     messages.INFO: '',
#
# }


#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru','Russian'),
    ('en','English'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'UTC'

USE_I18N = True
DATETIME_FORMAT="%Y-%m-%d%H:%M:%S"
USE_L10N = True

USE_TZ = False

MAX_ATTEMPTS=1
BACKGROUND_TASK_RUN_ASYNC = True

USE_L10N = False

PROJECT_ROOT = os.path.dirname(BASE_DIR)
STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static")
]


LOGIN_URL ='/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'baibakepc@gmail.com'
EMAIL_HOST_PASSWORD = 'cgS^Xv!Cc1Fn'

# FONTAWESOME_CSS_URL = '//cdn.example.com/fontawesome-min.css'  # absolute url
# # FONTAWESOME_CSS_URL = 'myapp/css/fontawesome.min.css'  # relative url
# FONTAWESOME_PREFIX = 'bg'

# HOSTS = ['.ngrok.io', '5a72b525ef0a', 'MBP-Viki','127.0.0.1', 'viki-GS63-7RD', 'DESKTOP-7QEV6BV', 'viki-Dell-System-XPS-15Z', 'viki-GS63-7RD', 'vn']
# print ("host="+socket.gethostname())
# if not socket.gethostname() in HOSTS:
RUN_MODE = "local"
# try:
#     if os.environ['RUN_MODE']:
#         RUN_MODE = os.environ['RUN_MODE']
# except Exception as e:
#     pass

if RUN_MODE == 'local':
    from .local import *
else:
    from .remote import *
    
# from .local import *