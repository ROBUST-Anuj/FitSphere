import json

from django.http import HttpResponse
from django.test import RequestFactory

import pytest

from apps.core.context import TenantContext
from apps.core.middleware import TenantResolutionMiddleware
from apps.core.models import Tenant

pytestmark = pytest.mark.django_db


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def tenant():
    return Tenant.objects.create(name="Iron Gym", slug="iron-gym")


def test_exempt_path_skips_tenant_resolution_entirely(factory):
    captured = {}

    def get_response(request):
        captured["tenant"] = TenantContext.get_or_none()
        return HttpResponse("ok")

    middleware = TenantResolutionMiddleware(get_response)
    request = factory.get("/api/health/")
    response = middleware(request)

    assert response.status_code == 200
    assert captured["tenant"] is None


def test_valid_tenant_header_binds_tenant_for_duration_of_request(factory, tenant):
    captured = {}

    def get_response(request):
        captured["tenant"] = TenantContext.get_or_none()
        return HttpResponse("ok")

    middleware = TenantResolutionMiddleware(get_response)
    request = factory.get("/api/workouts/", headers={"X-Tenant-ID": "iron-gym"})
    middleware(request)

    assert captured["tenant"] == tenant
    # Context is unbound again once the request/response cycle completes.
    assert TenantContext.get_or_none() is None


def test_unknown_tenant_header_returns_404_without_calling_view(factory):
    called = {"value": False}

    def get_response(request):
        called["value"] = True
        return HttpResponse("ok")

    middleware = TenantResolutionMiddleware(get_response)
    request = factory.get("/api/workouts/", headers={"X-Tenant-ID": "does-not-exist"})
    response = middleware(request)

    assert response.status_code == 404
    assert json.loads(response.content)["error"]["code"] == "tenant_not_found"
    assert called["value"] is False


def test_inactive_tenant_is_treated_as_not_found(factory):
    Tenant.objects.create(name="Closed Gym", slug="closed-gym", is_active=False)
    called = {"value": False}

    def get_response(request):
        called["value"] = True
        return HttpResponse("ok")

    middleware = TenantResolutionMiddleware(get_response)
    request = factory.get("/api/workouts/", headers={"X-Tenant-ID": "closed-gym"})
    response = middleware(request)

    assert response.status_code == 404
    assert called["value"] is False


def test_missing_tenant_header_passes_through_unbound(factory):
    captured = {}

    def get_response(request):
        captured["tenant"] = TenantContext.get_or_none()
        return HttpResponse("ok")

    middleware = TenantResolutionMiddleware(get_response)
    request = factory.get("/api/workouts/")
    response = middleware(request)

    assert response.status_code == 200
    assert captured["tenant"] is None
