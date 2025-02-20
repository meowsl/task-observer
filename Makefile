BACKEND_DIR = server

install-backend:
	@poetry env use 3.12.0
	@poetry install --no-root
	@make create-env

create-env:
	@poetry run python $(BACKEND_DIR)/config/set_env.py && echo .env successfully created

.PHONY: run-backend
run-backend:
	@poetry run uvicorn server.app:app --reload

.PHONY: makemigrations
makemigrations:
	@poetry run alembic revision --autogenerate


.PHONY: migrate
migrate:
	@poetry run alembic upgrade head

.PHONY: downgrade
downgrade:
	@poetry run alembic downgrade head