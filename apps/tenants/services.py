from __future__ import annotations

from django.db import transaction

from apps.core.models import Tenant
from apps.tenants.enums import MembershipRole
from apps.tenants.models import Membership


class MembershipService:
    """
    Membership business logic.
    """

    @staticmethod
    @transaction.atomic
    def add_member(
        *,
        tenant: Tenant,
        user,
        role: str = MembershipRole.MEMBER,
        invited_by=None,
    ) -> Membership:
        """
        Add a user to a tenant.
        """

        membership, created = Membership.objects.get_or_create(
            tenant=tenant,
            user=user,
            defaults={
                "role": role,
                "invited_by": invited_by,
                "is_active": True,
            },
        )

        if not created:
            membership.role = role
            membership.is_active = True
            membership.invited_by = invited_by
            membership.save(
                update_fields=[
                    "role",
                    "is_active",
                    "invited_by",
                ]
            )

        return membership

    @staticmethod
    @transaction.atomic
    def remove_member(
        *,
        membership: Membership,
    ) -> None:
        """
        Soft delete a membership.
        """

        membership.is_active = False

        membership.save(
            update_fields=[
                "is_active",
            ]
        )

    @staticmethod
    @transaction.atomic
    def change_role(
        *,
        membership: Membership,
        role: str,
    ) -> Membership:
        """
        Change a member's role.
        """

        membership.role = role

        membership.save(
            update_fields=[
                "role",
            ]
        )

        return membership
