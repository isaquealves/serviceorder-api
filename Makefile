.PHONY: help


.DEFAULT_GOAL := help

CURR_DIR := $(shell pwd)
container_name = service_order

help: ## This help.
	@echo "Install dependencies, build, run and clean containers in one just place"
	@echo ""
	@echo "Run any command with 	make <cmd>"
	@printf "\033[33m    %-10s\033[33m %s\n" "CMD" "Description"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m    %-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


build: ## Build the container
	-docker-compose -f docker-compose.yml up -d --build 
up: ## Set upt the container without starting it
	-docker-compose -f docker-compose.yml up --no-start
down: ## Remove the older container builds
	-docker-compose -f docker-compose.yml down
start: ## Starts the container
	-docker-compose start $(docker_container)
stop: ## Stops the container
	-docker-compose stop $(docker_container)
re: ## Rebuild all
	$(MAKE) stop down build up start
restart:
	$(MAKE) stop start