setup:
	pip install -r requirements.txt

init-migration:
	alembic revision --autogenerate -m "Initial migration"

migrations:
	alembic upgrade head

run:
	uvicorn app.main:app --reload

test:
	pytest --cov=app