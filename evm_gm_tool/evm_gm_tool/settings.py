"""
Django settings for evm_gm_tool project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os, re
from .env import *
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w_d9xqu97$8mj0aw1npo%yl@x-r357$_@%&kw4*8w8(bj6cd8w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ENV_ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [ 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tool'    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tool.middleware.LoginRequireMiddleware'
]

ROOT_URLCONF = 'evm_gm_tool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            #os.path.join(BASE_DIR, 'tool', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'project': 'tool.templatetags.project',
            }
            # 'loaders': [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader'
            # ]
        },
    },
]

WSGI_APPLICATION = 'evm_gm_tool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ENV_DB_DATABASE,
        'USER': ENV_DB_USERNAME,
        'PASSWORD': ENV_DB_PASSWORD,
        'HOST': ENV_DB_HOST,
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
print("{}             fdafadf".format(STATIC_ROOT))
# LOGIN_URL = '/tool/login/'
LOGOUT_URL = re.compile(r'^/logout$')
LOGIN_REDIRECT_URL = '/'

LOGIN_EXEMPLT_URLS = (
    re.compile(r'^login/$'),
)

ADMIN_URL = re.compile(r'^admin')

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MEDIA_URL = 'media/'
print(os.path.join(BASE_DIR, 'static/'))
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/')

SERVER_IP = ENV_SERVER_IP
SERVER_PORT = ENV_SERVER_PORT

PAGE_LIMIT = ENV_PAGE_LIMIT
