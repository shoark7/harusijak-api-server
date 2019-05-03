"""
Django settings for harusijak project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '64be&s0(ny#-c%ivl+9d!1-*^9)l)re0&-aptt-oa4d-y==3#d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',

    'date',
    'poet',
    'poem',
    'subject',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'harusijak.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'harusijak.wsgi.application'


# Password validation
# API server doesn't provide password validation
AUTH_PASSWORD_VALIDATORS = [
    # {
        # 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
        # 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
        # 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
        # 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# User model
AUTH_USER_MODEL = 'poet.Poet'



APPEND_SLASH = False

# Heroku setting
import django_heroku
django_heroku.settings(locals())


# S3 setting. It's long
AWS_STORAGE_BUCKET_NAME = 'harusijak-static-manage'
AWS_ACCESS_KEY_ID = os.environ['AwsAccessKey']
AWS_SECRET_ACCESS_KEY = os.environ['AwsSecretKey']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'harusijak.storage_backends.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_MEDIA_LOCATION = 'media'
# MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

AWS_POET_MEDIA_LOCATION = AWS_MEDIA_LOCATION + '/poets/'
POET_FILE_STORAGE = 'harusijak.storage_backends.PoetMediaStorage'

AWS_POEM_MEDIA_LOCATION = AWS_MEDIA_LOCATION + '/poems/'
POEM_FILE_STORAGE = 'harusijak.storage_backends.PoemMediaStorage'


# CORS
CORS_ORIGIN_ALLOW_ALL = True


# django-restframework 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth.custom_token.CustomTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if 'DATABASE_URL' in os.environ and 'DATABASE_PASSWORD' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dfioanc1psc2cm',
            'USER': 'gdoqfutxywvgmg',
            'PASSWORD': os.environ['DATABASE_PASSWORD'],
            'HOST': 'ec2-107-22-162-8.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }
    import dj_database_url

    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
