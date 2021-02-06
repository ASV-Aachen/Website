help:
	@echo "# Makefile Help #"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


start: ## Start network && build && docker-compose up
	./bin/start.sh

.PHONY: stop
stop: ## stop docker-compose and network
	./bin/stop.sh

clean: ## clean containers and images
	./bin/clean.sh

makemigrations: ## Generate Migrations for Django models
	./bin/makemigrations.sh	

migrate: ## Migrate Django models
	./bin/migrate.sh