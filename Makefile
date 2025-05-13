DB_CONTAINER_NAME=medol
APP_MODULE=src/medol/main.py

.PHONY: db-up db-down db-logs db-bash migrate-up migrate-down migrate-revision

db-up:
	docker compose up -d

db-down:
	docker compose down

db-logs:
	docker logs -f $(DB_CONTAINER_NAME)

db-bash:
	docker exec -it $(DB_CONTAINER_NAME) bash

migrate-up:
	alembic upgrade head

migrate-down:
	alembic downgrade -1

migrate-revision:
	alembic revision --autogenerate -m "$(name)"

run-dev:
	fastapi dev $(APP_MODULE)

run:
	fastapi $(APP_MODULE)