# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# Stage 1: builder — compiles wheels for all Python dependencies.
# Kept separate so the final image never contains gcc/dev headers.
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ /build/requirements/

ARG BUILD_ENV=local
RUN pip wheel --wheel-dir /build/wheels -r requirements/${BUILD_ENV}.txt

# ---------------------------------------------------------------------------
# Stage 2: runtime — minimal image, no compilers, runs as non-root.
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production

# libpq is needed at runtime to talk to Postgres (libpq-dev was only for compiling)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

ARG BUILD_ENV=local
COPY --from=builder /build/wheels /wheels
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements/${BUILD_ENV}.txt \
    && rm -rf /wheels

COPY --chown=appuser:appgroup . /app

RUN mkdir -p /app/staticfiles /app/mediafiles \
    && chown -R appuser:appgroup /app/staticfiles /app/mediafiles

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
