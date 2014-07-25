# -*- coding: utf-8 -*-


import os, sys
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_DIR, 'like_system/testapp'))

SECRET_KEY = 'django-like-systemTEST$3cr3t_KEY'
SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ROOT_URLCONF = 'like_system.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'like_system',
)

STATIC_ROOT = '/tmp/'  # Dummy
STATIC_URL = '/static/'