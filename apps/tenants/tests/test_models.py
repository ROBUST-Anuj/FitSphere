from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.core.models import Tenant
from apps.tenants.enums import MembershipRole
from apps.tenants.models import Membership

User = get_user_model()


class MembershipModelTests(TestCase):
    def test_create_membership(self):
        user = User.objects.create_user(
            email="member@test.com",
            password="Password@123",
        )

        tenant = Tenant.objects.create(
            name="Gym",
            slug="gym",
        )

        membership = Membership.objects.create(
            tenant=tenant,
            user=user,
            role=MembershipRole.MEMBER,
        )

        self.assertEqual(
            membership.role,
            MembershipRole.MEMBER,
        )

        self.assertTrue(membership.is_active)
