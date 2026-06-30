"""
Domain-level exceptions.

These carry zero Django/DRF imports on purpose: this module must be
importable from a plain Python script with no framework installed at all.
Framework-specific translation (e.g. "TenantNotFound -> HTTP 404") happens
in apps/core/exceptions.py, one layer up, never here.
"""


class DomainError(Exception):
    """Base class for all FitSphere domain errors."""


class TenantNotFoundError(DomainError):
    """Raised when a request references a tenant that does not exist or is inactive."""

    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"No active tenant found for identifier '{identifier}'.")


class TenantContextMissingError(DomainError):
    """
    Raised when tenant-scoped data is accessed without a tenant having been
    resolved for the current request/thread.

    This is a hard failure by design: silently returning an unscoped or
    empty queryset here would be exactly the kind of bug that leaks data
    across tenants. We'd rather raise loudly in development/CI than ship
    that bug to production.
    """

    def __init__(self):
        super().__init__(
            "Attempted to query tenant-scoped data with no tenant set in "
            "context. Use TenantContext.bind(tenant) or ensure "
            "TenantResolutionMiddleware ran for this request."
        )
