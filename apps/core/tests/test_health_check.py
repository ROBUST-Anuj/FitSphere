import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_health_check_is_reachable_without_authentication():
    client = APIClient()
    response = client.get("/api/health/")
    assert response.status_code == 200
    assert response.data["status"] == "healthy"
    assert response.data["checks"]["database"] is True


def test_health_check_is_exempt_from_tenant_header_requirement():
    # No X-Tenant-ID header sent at all — must still succeed.
    client = APIClient()
    response = client.get("/api/health/")
    assert response.status_code == 200
