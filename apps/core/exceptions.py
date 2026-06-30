"""
DRF-facing exception translation.

This is the one place in the codebase allowed to know both about our
framework-free domain exceptions (apps.core.domain.exceptions) AND about
DRF/HTTP. Views and services raise domain exceptions; this handler decides
what HTTP status/body that becomes. Keeping that mapping in one function
means the status code for "tenant not found" can't drift between endpoints.
"""

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_default_exception_handler

from apps.core.domain.exceptions import TenantContextMissingError, TenantNotFoundError

logger = logging.getLogger(__name__)

_DOMAIN_EXCEPTION_STATUS_MAP = {
    TenantNotFoundError: status.HTTP_404_NOT_FOUND,
    TenantContextMissingError: status.HTTP_400_BAD_REQUEST,
}


def custom_exception_handler(exc, context):
    for exc_type, http_status in _DOMAIN_EXCEPTION_STATUS_MAP.items():
        if isinstance(exc, exc_type):
            logger.info("Domain exception %s handled as HTTP %s", exc_type.__name__, http_status)
            return Response(
                {"error": {"code": exc_type.__name__, "message": str(exc)}},
                status=http_status,
            )

    # Anything we don't explicitly recognize (validation errors, DRF's own
    # exceptions, unexpected bugs) falls through to DRF's default handler,
    # which already produces sensible, consistent responses for those.
    return drf_default_exception_handler(exc, context)
