"""
Health check endpoint.

Used by Docker's HEALTHCHECK, load balancers, and uptime monitoring. It
deliberately checks real downstream dependencies (Postgres, Redis) rather
than just returning 200 unconditionally—a "healthy" response that doesn't
verify the database connection is misleading the moment Postgres goes down.
"""

from __future__ import annotations

import logging

from django.core.cache import cache
from django.db import connections
from django.db.utils import OperationalError

from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """
    Health check endpoint.

    This endpoint verifies that the application's critical dependencies
    (PostgreSQL and Redis) are reachable and functioning correctly.
    """

    # Monitoring systems should be able to access this endpoint without
    # authentication.
    permission_classes = [AllowAny]
    authentication_classes: list[type[BaseAuthentication]] = []

    def get(self, request: Request) -> Response:
        checks = {
            "database": self._check_database(),
            "cache": self._check_cache(),
        }

        all_healthy = all(checks.values())

        return Response(
            {
                "status": "healthy" if all_healthy else "unhealthy",
                "checks": checks,
            },
            status=(
                status.HTTP_200_OK
                if all_healthy
                else status.HTTP_503_SERVICE_UNAVAILABLE
            ),
        )

    @staticmethod
    def _check_database() -> bool:
        """
        Verify PostgreSQL connectivity.
        """
        try:
            connections["default"].cursor()
            return True
        except OperationalError:
            logger.exception("Database health check failed")
            return False

    @staticmethod
    def _check_cache() -> bool:
        """
        Verify Redis connectivity.
        """
        try:
            probe_key = "health_check_probe"

            cache.set(
                probe_key,
                "ok",
                timeout=5,
            )

            return cache.get(probe_key) == "ok"

        except Exception:  # noqa: BLE001
            logger.exception("Cache health check failed")
            return False