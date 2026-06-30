from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.core.models import Tenant
from apps.tenants.models import Membership

User = get_user_model()


def get_membership(*, tenant: Tenant, user) -> Membership | None:
    """
    Return a user's membership for a tenant.
    """
    return (
        Membership.objects.active()
        .filter(
            tenant=tenant,
            user=user,
        )
        .first()
    )


def get_members(*, tenant: Tenant) -> QuerySet[Membership]:
    """
    Return all active members of a tenant.
    """
    return Membership.objects.active().for_tenant(tenant)


def get_memberships_for_user(*, user) -> QuerySet[Membership]:
    """
    Return all active memberships of a user.
    """
    return Membership.objects.active().for_user(user)
