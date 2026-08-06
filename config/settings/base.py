# ✅ Toute la configuration commune
from pathlib import Path

from decouple import config

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# -----------------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------------

SECRET_KEY = config("SECRET_KEY")


# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "apps.core",
    "apps.accounts",
    "apps.expenses",
    "apps.dashboard",
    "theme"
]

THIRD_PARTY_APPS = [
    "tailwind",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

TAILWIND_APP_NAME = "theme"

INTERNAL_IPS = [
    "127.0.0.1",
]


APP_NAME = "Expense Tracker"

APP_VERSION = "0.1.0"

# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# -----------------------------------------------------------------------------
# URLs
# -----------------------------------------------------------------------------

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.app_settings",
            ],
        },
    },
]


# -----------------------------------------------------------------------------
# Authentication
# -----------------------------------------------------------------------------

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_URL = "accounts:login"

LOGIN_REDIRECT_URL = "dashboard:index"

LOGOUT_REDIRECT_URL = "accounts:login"


# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# -----------------------------------------------------------------------------
# Static files
# -----------------------------------------------------------------------------

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# -----------------------------------------------------------------------------
# Media files
# -----------------------------------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# -----------------------------------------------------------------------------
# Default primary key
# -----------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

