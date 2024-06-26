"""
Django settings for application project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from datetime import datetime
from pathlib import Path
from config.conf import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-9_t+69vx6i*8u_xvl32q^c=%rd&u*^rpih@p9ri7(r&#1=hu0l"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = locals().get("DEBUG", False)
ALLOWED_HOSTS = locals().get("ALLOWED_HOSTS", ["*"])


# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "apps.system",
    "apps.user",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "application.urls"
CORS_ALLOW_ALL_ORIGINS = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "static"),
            os.path.join(PROJECT_DIR, "web/dist/"), # for debug enabled
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "web/dist/"),
]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

WSGI_APPLICATION = "application.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": DATABASES_ENGINE,
        "NAME": DATABASES_NAME,
        "USER": DATABASES_USER,
        "PASSWORD": DATABASES_PASSWORD,
        "HOST": DATABASES_HOST,
        "PORT": DATABASES_PORT,
    }
}

TABLE_PREFIX = locals().get("TABLE_PREFIX", "")

AUTH_USER_MODEL = "user.User"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# LOGGING SETTINGS
LOG_PATH = os.path.join(BASE_DIR, "log")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] "
            "[%(levelname)s]- %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    # Define the specific way to handle logs
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(
                LOG_PATH, "all-{}.log".format(datetime.now().strftime("%Y-%m-%d"))
            ),
            "maxBytes": 1024 * 1024 * 5,  # file size
            "backupCount": 5,
            "formatter": "standard",
            "encoding": "utf-8",
        },
        # Output error logs
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(
                LOG_PATH, "error-{}.log".format(datetime.now().strftime("%Y-%m-%d"))
            ),
            "maxBytes": 1024 * 1024 * 5,  # file size
            "backupCount": 5,
            "formatter": "standard",
            "encoding": "utf-8",
        },
        # Output to console
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "standard",
        },
        # Output info logs
        "info": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(
                LOG_PATH, "info-{}.log".format(datetime.now().strftime("%Y-%m-%d"))
            ),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "standard",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        # Django handles all types of logs by default
        "django": {
            "handlers": ["default", "console"],
            "level": "INFO",
            "propagate": False,
        },
        # log needs to be passed as a parameter when called
        "log": {
            "handlers": ["error", "info", "console", "default"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# REST_FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "apps.system.utils.exception.CustomExceptionHandler",
}
from datetime import timedelta

ACCESS_TOKEN_LIFETIME = timedelta(hours=6)
REFRESH_TOKEN_LIFETIME = timedelta(days=1)

# JWT SETTINGS
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": ACCESS_TOKEN_LIFETIME,
    "REFRESH_TOKEN_LIFETIME": REFRESH_TOKEN_LIFETIME,
    "UPDATE_LAST_LOGIN": True,
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "user_email",
}

# SWAGGER SETTINGS

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"',
        },
    },
    "USE_SESSION_AUTH": False,
    "LOGIN_URL": "admin/",
    "LOGOUT_URL": "api/logout/",
    "APIS_SORTER": "alpha",
    "JSON_EDITOR": True,
    "OPERATIONS_SORTER": "alpha",
    "VALIDATOR_URL": None,
    "AUTO_SCHEMA_TYPE": 2,
}
# EMAIL SETTINGS
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = EMAIL_HOST
EMAIL_PORT = EMAIL_PORT
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_VALIDATION_TIME_LIMIT = locals().get("EMAIL_VALIDATION_TIME_LIMIT", 5)
EMAIL_WHITELIST = locals().get("EMAIL_WHITELIST", ["@*"])


# SUPER ADMIN SETTINGS
SUPER_ADMIN_EMAIL = locals().get("SUPER_ADMIN_EMAIL", "")
SUPER_ADMIN_USERNAME = locals().get("SUPER_ADMIN_USERNAME", "")
SUPER_ADMIN_PASSWORD = locals().get("SUPER_ADMIN_PASSWORD", "")