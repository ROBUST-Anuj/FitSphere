from __future__ import annotations

from rest_framework import serializers

from apps.tenants.models import Membership


class MembershipSerializer(serializers.ModelSerializer):
    """
    Membership response serializer.
    """

    user_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    tenant_name = serializers.CharField(
        source="tenant.name",
        read_only=True,
    )

    class Meta:
        model = Membership

        fields = (
            "id",
            "user",
            "user_email",
            "tenant",
            "tenant_name",
            "role",
            "is_active",
            "joined_at",
        )

        read_only_fields = (
            "id",
            "joined_at",
        )


class MembershipCreateSerializer(serializers.Serializer):
    """
    Invite/add member.
    """

    user_id = serializers.UUIDField()

    role = serializers.ChoiceField(choices=Membership._meta.get_field("role").choices)


class MembershipRoleSerializer(serializers.Serializer):
    """
    Change role serializer.
    """

    role = serializers.ChoiceField(choices=Membership._meta.get_field("role").choices)
