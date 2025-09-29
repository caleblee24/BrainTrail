.PHONY: up down logs api web psql seed migrate alembic_init

up:
	docker compose --env-file .env up --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

api:
	cd api && uvicorn app.main:create_app --host 0.0.0.0 --port 8000 --reload

web:
	cd web && npm run dev

psql:
	docker exec -it $$(docker ps -qf name=postgres) psql -U $$POSTGRES_USER -d $$POSTGRES_DB

seed:
	docker compose exec api python -m app.seed

alembic_init:
	cd api && alembic init alembic

migrate:
	cd api && alembic revision --autogenerate -m "init" && alembic upgrade head
