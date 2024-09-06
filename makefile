setup:
	pip install -r requirements.txt

init-migration:
	alembic revision --autogenerate -m "Initial migration"

migrations:
	alembic upgrade head

local:
	uvicorn app.main:app --reload --env-file .env.local

test/up:
	docker-compose --env-file .env.test --profile test up --build
	pytest --env-file .env.test

dev/up:
	docker-compose --env-file .env.dev --profile dev up --build
	uvicorn app.main:app --reload --env-file .env.dev

test:
	pytest --cov=app -s -v