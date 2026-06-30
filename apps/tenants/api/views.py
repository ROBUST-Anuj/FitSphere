from __future__ import annotations

from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.exceptions import NotFound

from apps.tenants.api.serializers import MembershipCreateSerializer, MembershipSerializer
from apps.tenants.permissions import IsTenantAdmin, IsTenantMember
from apps.tenants.selectors import get_members
from apps.tenants.services import MembershipService

User = get_user_model()


class MembershipListAPIView(generics.ListAPIView):
    """
    List members of current tenant.
    """

    serializer_class = MembershipSerializer
    permission_classes = [IsTenantMember]

    def get_queryset(self):
        return get_members(
            tenant=self.request.tenant,
        )


class MembershipCreateAPIView(generics.CreateAPIView):
    """
    Add member.
    """

    serializer_class = MembershipCreateSerializer
    permission_classes = [IsTenantAdmin]

    def perform_create(self, serializer):
        user = User.objects.filter(id=serializer.validated_data["user_id"]).first()

        if user is None:
            raise NotFound("User not found.")

        MembershipService.add_member(
            tenant=self.request.tenant,
            user=user,
            role=serializer.validated_data["role"],
            invited_by=self.request.user,
        )
