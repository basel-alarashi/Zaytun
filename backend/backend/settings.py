import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Loads backend/.env in development. In production, real environment
# variables should be set by the deployment platform instead — load_dotenv()
# is a no-op if the file doesn't exist, so this is safe either way.
load_dotenv(BASE_DIR / ".env")


def _get_env(name, default=None, required=False):
    """
    Read an environment variable with an explicit required/default contract.

    Failing loudly on a missing required variable is intentional: a silently
    applied insecure default is exactly the problem this replaces (NFR-012).
    """
    value = os.environ.get(name, default)
    if required and not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is not set. "
            f"Copy backend/.env.example to backend/.env and fill it in."
        )
    return value


SECRET_KEY = _get_env("DJANGO_SECRET_KEY", required=True)
DEBUG = _get_env("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = [
    host.strip()
    for host in _get_env("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "accounts",
    "api",
]

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": _get_env("DATABASE_NAME", required=True),
        "USER": _get_env("DATABASE_USER", required=True),
        "PASSWORD": _get_env("DATABASE_PASSWORD", required=True),
        "HOST": _get_env("DATABASE_HOST", "localhost"),
        "PORT": _get_env("DATABASE_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS settings
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in _get_env(
        "DJANGO_CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True

# CSRF / session cookie settings for a cross-port SPA (ADR-007)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in _get_env(
        "DJANGO_CSRF_TRUSTED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = _get_env("DJANGO_CSRF_COOKIE_SECURE", "False") == "True"
SESSION_COOKIE_SECURE = _get_env("DJANGO_SESSION_COOKIE_SECURE", "False") == "True"

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    # Session-based auth per ADR-007. No endpoints require authentication yet
    # (Sprint 2 introduces login/me and per-view permission classes).
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "accounts.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # Reshapes every DRF error response into the canonical
    # {"code", "message", "details"} contract from 10_API_Specification.md §12.
    "EXCEPTION_HANDLER": "api.exceptions.custom_exception_handler",
}

# Logging — ensures unexpected server errors are actually visible instead of
# silently vanishing (NFR-011).
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": _get_env("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

# Email
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

# Super User Credentails
# Email: basellogin9@gmail.com
# Password: Basel123
