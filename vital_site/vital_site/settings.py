"""
Django settings for vital_site project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import ConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = ConfigParser.ConfigParser()
config.read("/home/rdj259/config.ini")
# config.read("/Users/richie/vital-work")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get("Security", "SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'vital.apps.VitalConfig',
    'captcha',
    'passwords',
    'session_security',
    'jquery',
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vital_site.urls'

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

WSGI_APPLICATION = 'vital_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get("Database", "VITAL_DB_NAME"),
        'USER': config.get("Database", "VITAL_DB_USER"),
        'PASSWORD': config.get("Database", "VITAL_DB_PWD"),
        'HOST': config.get("Database", "VITAL_DB_HOST"),
        'PORT': config.get("Database", "VITAL_DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'vital.VLAB_User'
#AUTHENTICATION_BACKENDS = ['vital.backends.EmailAuthBackend', ]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/rdj259/vital_static'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/vital/vital.log',
            'formatter': 'verbose'
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'ERROR',
        },
        'vital': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = config.get("Email", "VITAL_EMAIL_HOST")
EMAIL_HOST_USER = config.get("Email", "VITAL_EMAIL_USER")
EMAIL_HOST_PASSWORD = config.get("Email", "VITAL_EMAIL_PWD")
EMAIL_PORT = config.get("Email", "VITAL_EMAIL_PORT")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PASSWORD_MIN_LENGTH = 8
PASSWORD_COMPLEXITY = {"UPPER":  1, "LOWER":  1, "DIGITS": 1, "SPECIAL": 1}

SESSION_COOKIE_AGE = 21600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SECURITY_WARN_AFTER = 21540
SESSION_SECURITY_EXPIRE_AFTER = SESSION_COOKIE_AGE

CRONJOBS = [
    # ('*/1 * * * *', 'vital.cron.force_logout_inactive_users', '>/tmp/stdout.log 2>/tmp/stderr.log'),
    # ('*/1 * * * *', 'vital.cron.clean_zombie_vms', '>/tmp/stdout.log 2>/tmp/stderr.log'),
    ('*/10 * * * * *', 'vital.cron.run_server_stats', '>/tmp/stdout.log 2>/tmp/stderr.log'),
]
