# FitSphere

Production-grade AI Fitness SaaS. Built incrementally following Clean
Architecture, Django REST Framework, PostgreSQL, Docker, Redis, Celery,
JWT auth, multi-tenancy, and RBAC.

## Week 1, Day 1 — what exists today

- Repository structure, Docker (multi-stage build, non-root runtime user)
- PostgreSQL + Redis via docker-compose, with healthchecks
- Django project split into `base/local/production/test` settings
- DRF configured: pagination, throttling, filtering, custom exception handler
- Celery wired end-to-end (broker, result backend, one verification task)
- `apps.core`: the shared foundation every future app builds on —
  `TimeStampedModel`, `Tenant`, `TenantAwareModel` + `TenantAwareManager`
  (automatic tenant scoping), `TenantResolutionMiddleware`, domain
  exceptions, a DB/cache-checking health endpoint
- Coding standards: black, isort, flake8, mypy (django-stubs), pre-commit,
  EditorConfig
- Tests: tenant model, tenant context, manager isolation, middleware,
  health check — `pytest --cov` configured with an 80% floor on `apps/`

**Explicitly out of scope today** (coming Day 2+): `apps.users`,
JWT authentication, RBAC/permissions, any actual fitness domain models. The
DRF `DEFAULT_AUTHENTICATION_CLASSES`/`DEFAULT_PERMISSION_CLASSES` in
`base.py` are deliberately strict (`IsAuthenticated`) even though no auth
backend exists yet — `local.py` relaxes this to `AllowAny` for local
development only, so we can build and test endpoints before JWT lands,
without weakening the production default.

## Architecture: why it's structured this way

**Clean Architecture boundary.** `apps/core/domain/` contains framework-free
Python (`exceptions.py` today; entities/value objects as the domain grows).
It must never import Django. Everything in `apps/core/models.py`,
`managers.py`, `middleware.py`, `views.py` is infrastructure/presentation
that depends on the domain layer, never the other way around. This is what
lets business rules be unit-tested with zero database and zero Django
runtime, and lets infrastructure (ORM, web framework) be replaced later
without touching business logic.

**Multi-tenancy: shared schema with enforced scoping.** Chosen over
schema-per-tenant / database-per-tenant for development speed and
operational simplicity at this stage (see chat history / ADR for full
tradeoff discussion). The risk this approach carries — a missed filter
leaking data across tenants — is mitigated structurally:

1. `TenantAwareModel` is the abstract base every tenant-scoped model must
   inherit. It adds `tenant` (FK) and overrides `objects` with
   `TenantAwareManager`.
2. `TenantAwareManager.get_queryset()` filters by the tenant bound in
   `TenantContext` automatically — `Model.objects.all()` is already scoped.
   No tenant in context → `TenantContextMissingError` is raised loudly
   rather than silently returning all rows or no rows.
3. `TenantContext` uses `contextvars` (not `threading.local`) so it stays
   correctly isolated per request even under ASGI/async.
4. `TenantResolutionMiddleware` resolves the tenant from the `X-Tenant-ID`
   header once per request and binds it for that request's lifetime only.
5. Genuinely cross-tenant operations (platform admin, billing
   reconciliation) call `.unscoped()` explicitly — a deliberate, greppable
   escape hatch, never the default.

**Settings split by environment, not by flag.** `DEBUG = True/False`
sprinkled through one settings.py with `if ENV == "prod"` branches is how
production accidentally inherits a dev-only setting. `local.py` and
`production.py` each import `base.py` and override only what's
environment-specific; there's no shared mutable state to get wrong.

## Running it locally

```bash
cp .env.example .env          # edit DJANGO_SECRET_KEY before anything else
make build
make up
make migrate
make ping-celery               # verifies web -> Redis -> celery_worker
```

- API: http://localhost:8000/api/health/
- Admin: http://localhost:8000/admin/
- Debug toolbar: enabled automatically in local settings

## Tests & linting

```bash
make test     # pytest, coverage enforced at 80% on apps/
make lint     # flake8 + black --check + isort --check-only
make format   # black + isort, auto-fix
```

`pre-commit install` once locally to run the same checks before every
commit (`.pre-commit-config.yaml`).

## Verifying tenant isolation manually

```bash
docker compose exec web python manage.py shell
>>> from apps.core.models import Tenant
>>> Tenant.objects.create(name="Iron Gym", slug="iron-gym")
```

Then:

```bash
curl http://localhost:8000/api/health/                       # no tenant needed
curl -H "X-Tenant-ID: iron-gym" http://localhost:8000/api/health/
curl -H "X-Tenant-ID: does-not-exist" http://localhost:8000/api/health/   # 404
```

## What's next (Day 2 preview)

`apps.users` with a custom `User` model (the first concrete
`TenantAwareModel`), `djangorestframework-simplejwt` configuration, login/
refresh endpoints, and the first RBAC permission classes built on top of
`TenantContext`.
