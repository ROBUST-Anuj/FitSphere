"""
Resolves which tenant a request is acting on behalf of, and binds it into
TenantContext for the lifetime of that request only.

Resolution strategy (Day 1): an explicit `X-Tenant-ID` header carrying the
tenant's slug. This is deliberately simple and explicit rather than
inferring tenant from subdomain — subdomain-based routing requires DNS/
wildcard cert setup we haven't done yet, and can be layered on top of this
same TenantContext mechanism later without touching any business logic,
since everything downstream just calls TenantContext.get().
"""

import logging

from django.conf import settings
from django.http import JsonResponse

from apps.core.context import TenantContext

logger = logging.getLogger(__name__)

# Paths that must work with no tenant context at all: platform admin and
# infrastructure endpoints that operate above/outside any single tenant.
TENANT_EXEMPT_PREFIXES = ("/admin", "/api/health")


class TenantResolutionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(TENANT_EXEMPT_PREFIXES):
            return self.get_response(request)

        tenant_slug = request.headers.get(settings.TENANT_HEADER_NAME)

        if not tenant_slug:
            # No tenant header on a tenant-scoped path: we don't reject here
            # because some endpoints (e.g. tenant signup) legitimately have
            # no tenant yet. Anything that genuinely needs a tenant will
            # raise TenantContextMissingError the moment it queries a
            # tenant-aware model, which the DRF exception handler turns into
            # a clear 400 response.
            return self.get_response(request)

        tenant = self._resolve_tenant(tenant_slug)
        if tenant is None:
            logger.warning("Rejected request for unknown/inactive tenant slug=%s", tenant_slug)
            return JsonResponse(
                {
                    "error": {
                        "code": "tenant_not_found",
                        "message": f"No active tenant '{tenant_slug}'.",
                    }
                },
                status=404,
            )

        with TenantContext.bind(tenant):
            return self.get_response(request)

    @staticmethod
    def _resolve_tenant(tenant_slug: str):
        from apps.core.models import Tenant

        try:
            return Tenant.objects.get(slug=tenant_slug, is_active=True)
        except Tenant.DoesNotExist:
            return None
