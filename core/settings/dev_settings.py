import os

from django.urls import reverse, reverse_lazy

from .core_settings import *

DEBUG = True
ALLOWED_HOSTS = ["0.0.0.0"]


# * prints SQL queries instantly
LOGGING = {
    "version": 1,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console"],
        }
    },
}


# django debug toolbar
INSTALLED_APPS += ("debug_toolbar",)  # type: ignore
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)  # type: ignore


# https://knasmueller.net/fix-djangos-debug-toolbar-not-showing-inside-docker
# needed for django toolbar to work in docker environment
import socket

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]


# * added because browsable api wont work with token authenttication
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += (  # type: ignore
    "rest_framework.authentication.SessionAuthentication",
)
# * test environment without mandatory email verification after registration through dj-rest-auth
ACCOUNT_EMAIL_VERIFICATION = "optional"

# redirect after newly registered user clicks on a link in the email
LOGIN_URL = reverse_lazy("api_root")  # ultimately url from the actual website
