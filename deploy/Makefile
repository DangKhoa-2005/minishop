# Convenience commands for clean deploy
.PHONY: build-clean up-clean down-clean seed-clean logs-clean

build-clean:
	docker-compose -f deploy/docker-compose.clean.yml build --no-cache

up-clean:
	docker-compose -f deploy/docker-compose.clean.yml up -d

down-clean:
	docker-compose -f deploy/docker-compose.clean.yml down

seed-clean:
	docker-compose -f deploy/docker-compose.clean.yml run backend_clean python seed.py

logs-clean:
	docker-compose -f deploy/docker-compose.clean.yml logs -f
