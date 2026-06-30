.PHONY: build up down restart logs shell migrate makemigrations test lint format superuser ping-celery

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart web

logs:
	docker compose logs -f web

shell:
	docker compose exec web python manage.py shell

bash:
	docker compose exec web bash

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

test:
	docker compose exec web pytest

lint:
	docker compose exec web flake8 .
	docker compose exec web black --check .
	docker compose exec web isort --check-only .

format:
	docker compose exec web black .
	docker compose exec web isort .

superuser:
	docker compose exec web python manage.py createsuperuser

ping-celery:
	docker compose exec web python manage.py shell -c "from apps.core.tasks import ping; print(ping.delay().get(timeout=5))"
