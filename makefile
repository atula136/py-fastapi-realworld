setup:
	pip install -r requirements.txt

init-migration:
	alembic revision --autogenerate -m "Initial migration"

migrations:
	alembic upgrade head

local:
	ENVIRONMENT=local alembic upgrade head
	ENVIRONMENT=local uvicorn app.main:app --reload --env-file .env.local

test/up:
	ENVIRONMENT=test docker-compose --env-file .env.test --profile test up --build -d

test/down:
	ENVIRONMENT=test docker-compose --env-file .env.test --profile test down -v

dev/up:
	ENVIRONMENT=dev alembic upgrade head
	ENVIRONMENT=dev docker-compose --env-file .env.dev --profile dev up -d
	ENVIRONMENT=dev uvicorn app.main:app --reload --env-file .env.dev

dev/down:
	ENVIRONMENT=dev docker-compose --env-file .env.dev --profile dev down

test:
	ENVIRONMENT=test python -m pytest --cov=app -s -v