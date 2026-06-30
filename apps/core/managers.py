"""
Tenant-scoping manager.

This is the core defense against cross-tenant data leaks in our shared
schema. Every model that inherits TenantAwareModel gets this manager as its
default `.objects`, meaning Model.objects.all() is ALREADY filtered to the
current tenant — a developer has to go out of their way (via `.unscoped()`)
to see data across tenants, rather than going out of their way to add a
filter. Secure defaults beat optional discipline.
"""

from django.db import models

from apps.core.context import TenantContext
from apps.core.domain.exceptions import TenantContextMissingError


class TenantAwareQuerySet(models.QuerySet):
    def unscoped(self) -> "TenantAwareQuerySet":
        """
        Explicitly opt out of tenant filtering.

        Reserved for genuinely cross-tenant operations: platform-level admin
        tooling, billing reconciliation jobs, support tooling used by
        FitSphere staff. Every call site using this method should have a
        comment justifying why crossing the tenant boundary is correct here.
        """
        return self

    def for_tenant(self, tenant) -> "TenantAwareQuerySet":
        return self.filter(tenant=tenant)


class TenantAwareManager(models.Manager):
    def get_queryset(self) -> TenantAwareQuerySet:
        base_qs = TenantAwareQuerySet(self.model, using=self._db)
        tenant = TenantContext.get_or_none()
        if tenant is None:
            # Fail loudly rather than silently returning all rows (or none).
            # See TenantContextMissingError docstring for the reasoning.
            raise TenantContextMissingError()
        return base_qs.filter(tenant=tenant)

    def unscoped(self) -> TenantAwareQuerySet:
        """Bypass tenant filtering entirely. Use sparingly and deliberately."""
        return TenantAwareQuerySet(self.model, using=self._db)
