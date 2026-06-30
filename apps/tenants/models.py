from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models

from apps.core.models import Tenant, TimeStampedModel
from apps.tenants.enums import MembershipRole
from apps.tenants.managers import MembershipManager


class Membership(TimeStampedModel):
    """
    Associates a user with a tenant.

    A single user may belong to multiple tenants and
    hold different roles in each tenant.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    role = models.CharField(
        max_length=20,
        choices=MembershipRole.choices,
        default=MembershipRole.MEMBER,
    )

    is_active = models.BooleanField(
        default=True,
    )

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sent_membership_invitations",
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    objects = MembershipManager()

    class Meta:
        ordering = [
            "tenant",
            "role",
            "user",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "tenant",
                    "user",
                ],
                name="unique_user_per_tenant",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "tenant",
                    "role",
                ],
            ),
            models.Index(
                fields=[
                    "user",
                ],
            ),
            models.Index(
                fields=[
                    "is_active",
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user.email} " f"({self.role}) @ " f"{self.tenant.name}"
