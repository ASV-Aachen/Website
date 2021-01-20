
help:
	@echo "# Makefile Help #"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

start: ## Start network && build && docker-compose up
	# docker network create traefik
	docker build -t webpageimage:local .
	docker-compose up -d

.PHONY: stop
stop: ## stop docker-compose and network
	docker-compose down
	# docker network rm traefik
