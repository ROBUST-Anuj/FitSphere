"""
Request-scoped tenant context.

We use `contextvars` rather than `threading.local` because Django can run
under ASGI (async views, channels later) where a single OS thread may
interleave multiple requests via different async tasks — threading.local
would leak tenant A's context into tenant B's coroutine in that scenario.
contextvars is correctly isolated per asyncio task as well as per thread.
"""

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Iterator, Optional

from apps.core.domain.exceptions import TenantContextMissingError

if TYPE_CHECKING:
    from apps.core.models import Tenant

_current_tenant: ContextVar[Optional["Tenant"]] = ContextVar("current_tenant", default=None)


class TenantContext:
    """Process-wide accessor for "which tenant is this request acting as right now"."""

    @staticmethod
    def set(tenant: "Tenant") -> None:
        _current_tenant.set(tenant)

    @staticmethod
    def get() -> "Tenant":
        """Return the bound tenant, or raise if none has been set."""
        tenant = _current_tenant.get()
        if tenant is None:
            raise TenantContextMissingError()
        return tenant

    @staticmethod
    def get_or_none() -> Optional["Tenant"]:
        return _current_tenant.get()

    @staticmethod
    def clear() -> None:
        _current_tenant.set(None)

    @staticmethod
    @contextmanager
    def bind(tenant: "Tenant") -> Iterator[None]:
        """
        Bind a tenant for the duration of a `with` block, restoring the
        previous value afterwards. Used by middleware per-request, and by
        management commands / Celery tasks that operate on a specific
        tenant outside of an HTTP request.
        """
        token = _current_tenant.set(tenant)
        try:
            yield
        finally:
            _current_tenant.reset(token)
