.PHONY: prod start build run down clean drop_db prune auto_backup stop_backup backup restore frontend_build frontend_export

BACKUP_COMMAND := "0 0 * * * cd \"$(PWD)\" && python3 scripts/backup.py"
DB_CONTAINER := postgres_songs
REDIS_CONTAINER := redis_songs
DB_VOLUME := $$(basename "$$(pwd)")_postgres_data
REDIS_VOLUME := $$(basename "$$(pwd)")_backend_data
APP_VOLUME := $$(basename "$$(pwd)")_redis_data

prod: down build

down:
	docker compose down

build:
	docker compose up -d --build --scale postgres_tests=0 --scale postgres=0
	
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
	make start

start:
	uvicorn src.main:app --reload

open-redis:
	docker exec -it $(REDIS_CONTAINER) redis-cli

clean:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf

auto_backup:
	@if crontab -l ; then \
		crontab -l > mycron ; \
	else \
		touch mycron ; \
	fi
	@echo $(BACKUP_COMMAND) >> mycron
	@crontab mycron
	@rm mycron
	@echo "Backup script added to cron"
	
stop_backup:
	crontab -l | grep -v -F $(BACKUP_COMMAND) | crontab -

backup:
	python3 scripts/backup.py
	@echo "Backup complete"

restore:
	python3 scripts/restore.py

drop_db: down 
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

prune: down
	docker system prune -a
	docker volume prune -a
