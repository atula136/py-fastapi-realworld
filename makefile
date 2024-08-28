setup:
	pip install -r requirements.txt

migrations:
	alembic upgrade head

run:
	uvicorn app.main:app --reload

test:
	pytest --cov=app