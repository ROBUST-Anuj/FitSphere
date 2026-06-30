"""
Celery application instance for FitSphere.

Imported by config/__init__.py so that `shared_task` decorated functions
register correctly regardless of how Django is started (runserver, gunicorn,
or the celery worker command itself).
"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("fitsphere")

# Pull CELERY_* settings straight from Django settings instead of
# maintaining a second, parallel configuration file.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover tasks.py in every installed app automatically — new apps don't
# need to be registered anywhere else to get their tasks picked up.
app.autodiscover_tasks()
