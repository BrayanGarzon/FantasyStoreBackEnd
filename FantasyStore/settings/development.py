from .common import *
import dj_database_url
import os
from .partials.util import get_secret

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p3gm=o9o+_r(5*o$$kn#h*8#n1r)aquf^^nm_v5u0pn^qa$=4*'

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['app-django.dev.byteobe.com', 'localhost', '127.0.0.1', '10.0.2.2', '*']

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# URL base
BASE_URL = 'https://fantasystorebackend-79vb.onrender.com'

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True



PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": os.environ.get('FCM_API_KEY', ''),
    "APNS_CERTIFICATE": "./certs/aps.pem",
    "APNS_USE_SANDBOX": True,
    "APNS_TOPIC": "co.altix.chilazi",
}

SOCKET_SERVICE_URL = os.environ.get('SOCKET_SERVICE_URL', '')

# CORS Config: install django-cors-headers and uncomment the following to allow CORS from any origin

DEV_APPS = [
    'corsheaders'
]

INSTALLED_APPS += DEV_APPS

DEV_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware'
]

MIDDLEWARE = MIDDLEWARE + DEV_MIDDLEWARE  # CORS middleware should be at the top of the list

CORS_ORIGIN_ALLOW_ALL = True


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# Configured with DATABASE_URL env, usually from dokku
if os.environ.get('DATABASE_URL', ''):
    DATABASES = {
        'default': dj_database_url.config()
    }
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'fantasystore',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
        }
    }

# Simple JWT
SIMPLE_JWT.update({
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
    'SIGNING_KEY': SECRET_KEY,
})


PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": os.environ.get('FCM_API_KEY', ''),
    # "APNS_CERTIFICATE": "./certs/aps-dev.pem",
    "APNS_AUTH_KEY_PATH": os.environ.get('APNS_AUTH_KEY_PATH', ''),
    "APNS_AUTH_KEY_ID": os.environ.get('APNS_AUTH_KEY_ID', ''),
    "APNS_TEAM_ID": os.environ.get('APNS_TEAM_ID', ''),
    "APNS_TOPIC": os.environ.get('APNS_TOPIC', ''),
    "APNS_USE_SANDBOX": True,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}

API_FIREBASE_KEY = os.environ.get('API_FIREBASE_KEY', '')

SPECTACULAR_SETTINGS['SERVERS'] = [{"url": "http://localhost:8000"}, {"url": BASE_URL}]

PASSWORD_RESET_EXPIRE_DAYS = 1

## S3
if get_secret('AWS_ACCESS_KEY_ID'):
    AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = get_secret("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = get_secret("AWS_S3_REGION_NAME")  # ej: "us-east-1"

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Ruta de archivos media (user uploaded)
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

    DEFAULT_FILE_STORAGE = 'FantasyStore.storage_backends.MediaStorage'

    # Opcional: Deshabilitar ACLs
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False  # URLs no firmadas

