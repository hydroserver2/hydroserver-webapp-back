import datetime
import os
import dj_database_url
from pathlib import Path

from corsheaders.defaults import default_headers
from pydantic import BaseSettings, PostgresDsn, EmailStr, HttpUrl
from typing import Union
from django.contrib.admin.views.decorators import staff_member_required
from decouple import config, UndefinedValueError

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default=None)
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default=None)
# AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = 'admin@hydroserver.ciroh.org'

try:
    GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY')
except UndefinedValueError:
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

try:
    LOCAL_CSV_STORAGE = config('LOCAL_CSV_STORAGE')
except UndefinedValueError:
    LOCAL_CSV_STORAGE = '~/'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class EnvironmentSettings(BaseSettings):
    """
    Defines Django environment variables.

    The default settings defined here should only be used in development environments and are not suitable for
    production. In production environments, these settings should be defined using environment variables or a .env file
    in the root project directory.
    """

    # TODO Find/create types for other databases. In the meantime, allow str.
    PROXY_BASE_URL: str = 'http://127.0.0.1:8000'
    ALLOWED_HOSTS: str = '127.0.0.1,localhost'
    CORS_ALLOWED_ORIGINS: str = 'http://127.0.0.1:5173,http://localhost:5173'
    DATABASE_URL: Union[PostgresDsn, str] = f'sqlite:///{BASE_DIR}/db.sqlite3'
    CONN_MAX_AGE: int = 600
    CONN_HEALTH_CHECKS: bool = True
    SSL_REQUIRED: bool = False
    SECRET_KEY: str = 'django-insecure-zw@4h#ol@0)5fxy=ib6(t&7o4ot9mzvli*d-wd=81kjxqc!5w4'
    DEBUG: bool = True
    OAUTH_ORCID_CLIENT: str = ''
    OAUTH_ORCID_SECRET: str = ''
    OAUTH_GOOGLE_CLIENT: str = ''
    OAUTH_GOOGLE_SECRET: str = ''

    class Config:
        env_file = f'{BASE_DIR}/.env'
        case_sensitive = True


env_config = EnvironmentSettings()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_config.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_config.DEBUG

PROXY_BASE_URL = env_config.PROXY_BASE_URL

ALLOWED_HOSTS = env_config.ALLOWED_HOSTS.split(',')

CORS_ALLOWED_ORIGINS = env_config.CORS_ALLOWED_ORIGINS.split(',') if hasattr(env_config, 'CORS_ALLOWED_ORIGINS') else ['http://localhost:5173']

CORS_ALLOW_HEADERS = list(default_headers) + [
    'Refresh_Authorization',
]

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=15),
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sites.apps.SitesConfig',
    'accounts.apps.AccountsConfig',
    'django_ses',
    'django_vite',
    'sensorthings',
    'rest_framework',
    'ninja',
    'ninja_extra',
    # 'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hydrothings.middleware.SensorThingsMiddleware'
]

ROOT_URLCONF = 'hydroserver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'hydroserver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

os.environ["DATABASE_URL"] = env_config.DATABASE_URL

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=env_config.CONN_MAX_AGE,
        conn_health_checks=env_config.CONN_HEALTH_CHECKS,
        ssl_require=env_config.SSL_REQUIRED
    )
}

LOGIN_REDIRECT_URL = 'sites'
LOGOUT_REDIRECT_URL = 'home'
AUTH_USER_MODEL = 'accounts.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
STATIC_ROOT = 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Vite Settings

DJANGO_VITE_ASSETS_PATH = BASE_DIR / 'frontend' / 'dist'
DJANGO_VITE_MANIFEST_PATH = DJANGO_VITE_ASSETS_PATH / 'vite' / 'manifest.json'
DJANGO_VITE_STATIC_URL_PREFIX = 'vite'

STATICFILES_DIRS += [DJANGO_VITE_ASSETS_PATH]

# SensorThings API Settings

STAPI_TITLE = 'HydroServer SensorThings API'
STAPI_DESCRIPTION = '''
    The HydroServer API can be used to create and update monitoring site metadata, and post
    results data to HydroServer data stores.
'''
STAPI_VERSION = '1.1'

FROST_BASE_URL = 'http://localhost:8080/FROST-Server'


AUTHLIB_OAUTH_CLIENTS = {
    'orcid': {
        'client_id': env_config.OAUTH_ORCID_CLIENT,
        'client_secret': env_config.OAUTH_ORCID_SECRET,
        'server_metadata_url': 'https://sandbox.orcid.org/.well-known/openid-configuration'
    },
    'google': {
        'client_id': env_config.OAUTH_GOOGLE_CLIENT,
        'client_secret': env_config.OAUTH_GOOGLE_SECRET,
        'server_metadata_url': 'https://accounts.google.com/.well-known/openid-configuration'
    }
}
