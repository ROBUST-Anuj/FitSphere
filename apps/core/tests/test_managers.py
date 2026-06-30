"""
These tests exist to prove the single most safety-critical guarantee in a
shared-schema multi-tenant system: a query for tenant A can never return
tenant B's rows, and querying with no tenant bound fails loudly instead of
silently returning the wrong thing.

_DummyTenantScopedRecord is a test-only concrete model (TenantAwareModel is
abstract and can't be queried directly). Its table is created for the
duration of each test's transaction via schema_editor and is rolled back
automatically by pytest-django's per-test transaction — no manual teardown
needed, and it never appears in real migrations.
"""

from django.db import connection, models

import pytest

from apps.core.context import TenantContext
from apps.core.domain.exceptions import TenantContextMissingError
from apps.core.models import Tenant, TenantAwareModel

pytestmark = pytest.mark.django_db


class DummyTenantScopedRecord(TenantAwareModel):
    label = models.CharField(max_length=100)

    class Meta:
        app_label = "core"
        managed = False


@pytest.fixture
def dummy_table():
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(DummyTenantScopedRecord)
    yield DummyTenantScopedRecord


def test_manager_raises_without_tenant_context(dummy_table):
    with pytest.raises(TenantContextMissingError):
        list(dummy_table.objects.all())


def test_manager_scopes_queries_to_current_tenant(dummy_table):
    tenant_a = Tenant.objects.create(name="Gym A", slug="gym-a")
    tenant_b = Tenant.objects.create(name="Gym B", slug="gym-b")

    with TenantContext.bind(tenant_a):
        dummy_table.objects.create(tenant=tenant_a, label="a1")
    with TenantContext.bind(tenant_b):
        dummy_table.objects.create(tenant=tenant_b, label="b1")

    with TenantContext.bind(tenant_a):
        labels = list(dummy_table.objects.values_list("label", flat=True))
    assert labels == ["a1"]

    with TenantContext.bind(tenant_b):
        labels = list(dummy_table.objects.values_list("label", flat=True))
    assert labels == ["b1"]


def test_unscoped_explicitly_bypasses_tenant_filtering(dummy_table):
    tenant_a = Tenant.objects.create(name="Gym A", slug="gym-a")
    tenant_b = Tenant.objects.create(name="Gym B", slug="gym-b")

    with TenantContext.bind(tenant_a):
        dummy_table.objects.create(tenant=tenant_a, label="a1")
    with TenantContext.bind(tenant_b):
        dummy_table.objects.create(tenant=tenant_b, label="b1")

    assert dummy_table.objects.unscoped().count() == 2
