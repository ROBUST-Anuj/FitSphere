from __future__ import annotations

from django.db import models

from apps.tenants.enums import MembershipRole


class MembershipQuerySet(models.QuerySet):
    """
    Custom queryset for Membership.
    """

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def owners(self):
        return self.filter(role=MembershipRole.OWNER)

    def admins(self):
        return self.filter(role=MembershipRole.ADMIN)

    def trainers(self):
        return self.filter(role=MembershipRole.TRAINER)

    def members(self):
        return self.filter(role=MembershipRole.MEMBER)

    def for_tenant(self, tenant):
        return self.filter(tenant=tenant)

    def for_user(self, user):
        return self.filter(user=user)


MembershipManager = models.Manager.from_queryset(MembershipQuerySet)
