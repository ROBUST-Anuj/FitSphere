from __future__ import annotations

from rest_framework.permissions import BasePermission

from apps.tenants.enums import MembershipRole
from apps.tenants.selectors import get_membership


class IsTenantMember(BasePermission):
    """
    User must belong to the current tenant.
    """

    def has_permission(self, request, view):
        tenant = getattr(request, "tenant", None)

        if tenant is None:
            return False

        membership = get_membership(
            tenant=tenant,
            user=request.user,
        )

        return membership is not None


class IsTenantAdmin(BasePermission):
    """
    User must be ADMIN or OWNER.
    """

    def has_permission(self, request, view):
        tenant = getattr(request, "tenant", None)

        if tenant is None:
            return False

        membership = get_membership(
            tenant=tenant,
            user=request.user,
        )

        if membership is None:
            return False

        return membership.role in (
            MembershipRole.OWNER,
            MembershipRole.ADMIN,
        )


class IsTenantOwner(BasePermission):
    """
    User must be OWNER.
    """

    def has_permission(self, request, view):
        tenant = getattr(request, "tenant", None)

        if tenant is None:
            return False

        membership = get_membership(
            tenant=tenant,
            user=request.user,
        )

        if membership is None:
            return False

        return membership.role == MembershipRole.OWNER
