.PHONY: prod start build run down clean backup fake_data open-redis _drop_db _prune

DB_CONTAINER := postgres_songs
REDIS_CONTAINER := redis_songs
DB_VOLUME := $$(basename "$$(pwd)")_postgres_data
REDIS_VOLUME := $$(basename "$$(pwd)")_backend_data
APP_VOLUME := $$(basename "$$(pwd)")_redis_data

prod: down build

down:
	docker compose down

build:
	docker compose up -d --build --scale postgres_tests=0

run: down
	docker compose up postgres redis -d
	@while true; do \
		sleep 1; \
		result_db=$$(docker inspect -f '{{json .State.Health.Status}}' $(DB_CONTAINER)); \
		result_redis=$$(docker inspect -f '{{json .State.Health.Status}}' $(REDIS_CONTAINER)); \
		if [ "$$result_db" = "\"healthy\"" ] && [ "$$result_redis" = "\"healthy\"" ]; then \
			echo "Services are healthy"; \
			break; \
		fi; \
	done
	alembic upgrade head
	make fake_data
	make start

start:
	uvicorn src.main:app --reload

fake_data:
	python3 -m scripts.initial_db
	@echo "fake data has added successfully"

open-redis:
	docker exec -it $(REDIS_CONTAINER) redis-cli

clean:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf

backup:
	python3 scripts/backup.py
	@echo "Backup complete"

restore:
	python3 scripts/restore.py
	@echo "Restore backup complete"

_drop_db: down 
	if docker volume ls -q | grep -q $(DB_VOLUME); then \
		docker volume rm $(DB_VOLUME); \
		echo "successfully drop_db 1";\
	fi
	if docker volume ls -q | grep -q $(REDIS_VOLUME); then \
		docker volume rm $(REDIS_VOLUME); \
		echo "successfully drop_db 2";\
	fi
	if docker volume ls -q | grep -q $(APP_VOLUME); then \
		docker volume rm $(APP_VOLUME); \
		echo "successfully drop_db 3";\
	fi

_prune: down
	docker system prune -a
	docker volume prune -a
