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

firstStart: ## Create the init Data
	./bin/firstStart.sh

createTestData: ## Creates Test Users and News
	./bin/TestData.sh

update: ## Pulls the Update and starts the migration Process
	./bin/update.sh

startAutoFigures: ## Starts the Cron Skripts
	./bin/cronJobs.sh

updateFromKeycloak: ## Gets the Data from Keyclaok and updates the Webservice
	./bin/updateKeycloak.sh

createRootUser: ## Create a superuser for Django
	./bin/superuser.sh

setupFirstStart: ## Script for the initial start
	./bin/setupFirstStart.sh