from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.core.models import Tenant
from apps.tenants.enums import MembershipRole
from apps.tenants.services import MembershipService

User = get_user_model()


class MembershipServiceTests(TestCase):
    def test_add_member(self):
        user = User.objects.create_user(
            email="member@test.com",
            password="Password@123",
        )

        tenant = Tenant.objects.create(
            name="Gym",
            slug="gym",
        )

        membership = MembershipService.add_member(
            tenant=tenant,
            user=user,
            role=MembershipRole.TRAINER,
        )

        self.assertEqual(
            membership.role,
            MembershipRole.TRAINER,
        )
