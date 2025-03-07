"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import environ
import mongoengine

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / ".env"

if env_path.exists():
    with env_path.open("rt", encoding="utf8") as f:
        env.read_env(f)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^ycm=3o-d1g(4suic-$hu896&7msuf=%!sx1shu(5)qz@b8(cg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    'popping.world',
    'www.popping.world',
    '127.0.0.1',
    '14.35.210.5'
]

AUTH_USER_MODEL = 'user.User'

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'user',
    'share',
    'popup',
    'map',
    'register',
]

MONGO_DB_NAME = env('MONGO_DB_NAME')
MONGO_URI = env('MONGO_URL')

mongoengine.connect(db=MONGO_DB_NAME, host=MONGO_URI)

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

SESSION_COOKIE_AGE = 2592000  # 30일 (단위 : 초)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env('POSTGRES_DATABASE_NAME'),
#         'USER': env('POSTGRES_USER_NAME'),
#         'PASSWORD': env('POSTGRES_USER_PASSWORD'),
#         'HOST': env('POSTGRES_HOST'),
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('MARIADB_DATABASE_NAME'),
        'USER': env('MARIADB_USER_NAME'),
        'PASSWORD': env('MARIADB_USER_PASSWORD'),
        'HOST': env('MARIADB_HOST'),
        'PORT': '3306',

    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Config
CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "credentials",
    "host",
    "origin",
    "X-CSRFToken",
    "x-csrftoken",
    "csrftoken",
    "x-requested-with",
)

CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    'https://popping.world',
    'https://www.popping.world',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

## CSRF_COOKIE_NAME 원래 기본 값 => csrftoken
## CSRF_HEADER_NAME 원래 기본 값 => HTTP_X_CSRFTOKEN
# CSRF_COOKIE_NAME = 'XSRF-TOKEN'
# CSRF_HEADER_NAME = 'X-XSRF-TOKEN'

# Email Config
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'app.popping@gmail.com'
EMAIL_HOST_PASSWORD = 'bblsqfukecmuxrxz'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
