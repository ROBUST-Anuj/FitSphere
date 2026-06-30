"""
Injects the current tenant's slug into every log record so production logs
can be grepped/filtered per tenant when debugging a specific customer's
issue — without every single log call having to remember to pass it in.
"""

import logging

from apps.core.context import TenantContext


class TenantContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        tenant = TenantContext.get_or_none()
        record.tenant = tenant.slug if tenant is not None else "-"
        return True
