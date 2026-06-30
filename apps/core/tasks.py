"""
apps.core has one task today: a liveness probe for the Celery pipeline
itself. Business-domain tasks (e.g. sending workout reminders) will live in
their owning app's tasks.py once that app exists, picked up automatically
by Celery's autodiscover_tasks().
"""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="core.ping")
def ping() -> str:
    """
    Round-trips through Redis and back. Used to confirm, after `docker
    compose up`, that web -> Redis -> celery_worker is wired correctly:

        docker compose exec web python manage.py shell
        >>> from apps.core.tasks import ping
        >>> ping.delay().get(timeout=5)
        'pong'
    """
    logger.info("Celery ping task executed")
    return "pong"
