"""
Django settings for productsapi project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
from urllib import request

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8z4ca&cxh2oyrm#3h9z_ikboy8u&qb-*gndg9l!i)d2xua5@v@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':
    json_data = open('zappa_settings.json')
    env_vars = json.load(json_data)['dev']['aws_environment_variables']
    for key, val in env_vars.items():
        os.environ[key] = val


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'products',
    'books',
    'core',
    'users',
    'django_s3_storage',
    'drf_yasg'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

ROOT_URLCONF = 'productsapi.urls'

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

WSGI_APPLICATION = 'productsapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tokhna',
            'USER': 'admin',
            'PASSWORD': 'FdLBESvOoLAjbK7zaDgf',
            'HOST': 'tokhna.cdn7wdipzauc.us-east-1.rds.amazonaws.com',
            'PORT': '3306',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if 'COGNITO_AWS_REGION' in os.environ:
    COGNITO_AWS_REGION = os.environ['COGNITO_AWS_REGION']
    COGNITO_USER_POOL = os.environ['COGNITO_USER_POOL']
    # Provide this value if `id_token` is used for authentication (it contains 'aud' claim).
    # `access_token` doesn't have it, in this case keep the COGNITO_AUDIENCE empty
    COGNITO_AUDIENCE = os.environ['COGNITO_AUDIENCE']
    COGNITO_POOL_URL = None  # will be set few lines of code later, if configuration provided

    rsa_keys = {}
    # To avoid circular imports, we keep this logic here.
    # On django init we download jwks public keys which are used to validate jwt tokens.
    # For now there is no rotation of keys (seems like in Cognito decided not to implement it)
    if COGNITO_AWS_REGION and COGNITO_USER_POOL:
        COGNITO_POOL_URL = 'https://cognito-idp.{}.amazonaws.com/{}'.format(COGNITO_AWS_REGION, COGNITO_USER_POOL)
        pool_jwks_url = COGNITO_POOL_URL + '/.well-known/jwks.json'
        jwks = json.loads(request.urlopen(pool_jwks_url).read())
        rsa_keys = {key['kid']: json.dumps(key) for key in jwks['keys']}


    JWT_AUTH = {
        'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'core.utils.jwt.get_username_from_payload_handler',
        'JWT_DECODE_HANDLER': 'core.utils.jwt.cognito_jwt_decode_handler',
        'JWT_PUBLIC_KEY': rsa_keys,
        'JWT_ALGORITHM': 'RS256',
        'JWT_AUDIENCE': COGNITO_AUDIENCE,
        'JWT_ISSUER': COGNITO_POOL_URL,
        'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

USE_S3 = os.environ.get('USE_S3') == 'TRUE'

if USE_S3:
    YOUR_S3_BUCKET = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
    AWS_S3_BUCKET_NAME_STATIC = YOUR_S3_BUCKET
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % YOUR_S3_BUCKET
    STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
