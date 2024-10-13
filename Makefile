run:
	@uvicorn pizzaria_api.main:app --reload

create-migrations:
	@alembic revision --autogenerate -m "migration message"

run-migrations:
	@alembic upgrade head



