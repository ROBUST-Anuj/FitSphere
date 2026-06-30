import pytest

from apps.core.context import TenantContext
from apps.core.domain.exceptions import TenantContextMissingError
from apps.core.models import Tenant

pytestmark = pytest.mark.django_db


class TestTenantModel:
    def test_creates_tenant_with_unique_slug(self):
        tenant = Tenant.objects.create(name="Iron Gym", slug="iron-gym")
        assert tenant.id is not None
        assert tenant.is_active is True

    def test_slug_uniqueness_is_enforced(self):
        Tenant.objects.create(name="Iron Gym", slug="iron-gym")
        with pytest.raises(Exception):
            Tenant.objects.create(name="Iron Gym Duplicate", slug="iron-gym")


class TestTenantContext:
    def test_get_or_none_returns_none_when_unbound(self):
        assert TenantContext.get_or_none() is None

    def test_get_raises_when_unbound(self):
        with pytest.raises(TenantContextMissingError):
            TenantContext.get()

    def test_bind_sets_and_restores_previous_context(self):
        tenant_a = Tenant.objects.create(name="Gym A", slug="gym-a")
        tenant_b = Tenant.objects.create(name="Gym B", slug="gym-b")

        with TenantContext.bind(tenant_a):
            assert TenantContext.get() == tenant_a
            with TenantContext.bind(tenant_b):
                assert TenantContext.get() == tenant_b
            # Restored to tenant_a after the inner block exits.
            assert TenantContext.get() == tenant_a

        # Restored to unbound after the outer block exits.
        assert TenantContext.get_or_none() is None
