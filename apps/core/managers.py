"""
Tenant-scoping manager.

This is the core defense against cross-tenant data leaks in our shared
schema. Every model that inherits TenantAwareModel gets this manager as its
default `.objects`.
"""

from django.db import models

from apps.core.context import TenantContext
from apps.core.domain.exceptions import TenantContextMissingError


class TenantAwareQuerySet(models.QuerySet):
    """
    QuerySet for tenant-aware models.
    """

    def unscoped(self):
        return self

    def for_tenant(self, tenant):
        return self.filter(
            tenant=tenant,
        )


class TenantAwareManager(models.Manager):
    """
    Default manager that automatically scopes queries
    to the current tenant.
    """

    def get_queryset(self):
        queryset = TenantAwareQuerySet(
            self.model,
            using=self._db,
        )

        tenant = TenantContext.get_or_none()

        if tenant is None:
            raise TenantContextMissingError()

        return queryset.filter(
            tenant=tenant,
        )

    def unscoped(self):
        return TenantAwareQuerySet(
            self.model,
            using=self._db,
        )
