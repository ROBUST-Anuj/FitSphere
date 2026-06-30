"""
Core abstract base models.

Two distinct abstractions live here:

- TimeStampedModel: generic auditing fields every model wants (id, created,
  updated). Has nothing to do with tenancy.
- TenantAwareModel: adds the tenant FK + scoped manager. Every future
  business model (User, WorkoutPlan, Exercise, Subscription...) will
  inherit from this, NOT from TimeStampedModel directly, unless it is
  explicitly platform-global data.

Tenant itself inherits TimeStampedModel but NOT TenantAwareModel — a tenant
cannot belong to itself, that would be a circular scoping problem.
"""

import uuid

from django.db import models

from apps.core.managers import TenantAwareManager


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Tenant(TimeStampedModel):
    """
    A FitSphere customer organization (a gym, a personal-training studio, a
    corporate wellness program, etc). Every tenant-scoped row in the system
    points back here via TenantAwareModel.tenant.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=63, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TenantAwareModel(TimeStampedModel):
    """
    Abstract base for every model whose data must never be visible across
    tenant boundaries. Subclassing this and nothing else is what makes a
    model "tenant-scoped" throughout the system.
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
    )

    objects = TenantAwareManager()

    class Meta(TimeStampedModel.Meta):
        abstract = True
