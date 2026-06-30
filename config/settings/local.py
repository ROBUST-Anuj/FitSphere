"""Local development settings."""

import sys

from decouple import Csv, config

from .base import *  # noqa: F401,F403

DEBUG = True

ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS",
    cast=Csv(),
    default="localhost,127.0.0.1",
)

# -----------------------------------------------------------------------------
# Development Apps
# -----------------------------------------------------------------------------

INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
]

if "test" not in sys.argv:
    INSTALLED_APPS += [  # noqa: F405
        "debug_toolbar",
    ]

# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------

if "test" not in sys.argv:
    MIDDLEWARE = [  # noqa: F405
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,  # noqa: F405
    ]

INTERNAL_IPS = [
    "127.0.0.1",
]

# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = True

# -----------------------------------------------------------------------------
# REST Framework
# -----------------------------------------------------------------------------

REST_FRAMEWORK = {  # noqa: F405
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
