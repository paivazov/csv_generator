.DEFAULT_GOAL := start


# the `make` command may be run anywhere, we need the Makefile's directory
# to build properly path to involved files
THIS_DIR := $(abspath $(dir $(firstword $(MAKEFILE_LIST))))
YAML_FILES := -f ./app/docker-compose.yml \
              -f ./docker-compose.yml

ifneq ($(wildcard $(THIS_DIR)/.env.local), )
	EXTRA_ENV_FILE := --env-file='$(THIS_DIR)/.env.local'
endif

DOCKER=docker-compose $(YAML_FILES) $(EXTRA_ENV_FILE)


.PHONY: start config stop clean requirements

start:
	$(DOCKER) up

# to check final docker-compose file you may use this target
config:
	$(DOCKER) config

stop:
	$(DOCKER) stop

clean: stop
	$(DOCKER) down --remove-orphans --volumes

requirements:
	$(DOCKER) run --rm application make dev-requirements


.PHONY: test test_ui test_app

test: test_app


test_app:
	$(DOCKER) run --rm application make quicktest


.PHONY: check_full check check_ui check_app format_app

check_full: check test

check:  check_app



check_app:
	$(DOCKER) run --rm application make check

format_app:
	$(DOCKER) run --rm application make format


migrations:
	$(DOCKER) up -d postgres
	$(DOCKER) run --rm api make migrations
	$(DOCKER) stop postgres

load_data:
	$(DOCKER) up -d postgres
	$(DOCKER) run --rm api make load_data
	$(DOCKER) stop postgres

# Django's "manage.py" tool has too many commands to extract them into separate
# targets. At the same time we do need those commands from time to time.
# Problem here is that many command depends on database (like `manage.py
# createsuperuser`) or other services moved into separate containers. To solve
# this conflict you may use the `visit_to_backend` target. It runs all required
# services/containers, and opens to you a `/bin/bash` session inside the
# `backend` container. After you finish your job inside "backend" container and
# hits the "exit" command (or just Ctrl+D) this target gracefully stops all
# dependent containers
visit_to_backend:
	$(DOCKER) up -d postgres
	$(DOCKER) run --rm api /bin/bash
	$(DOCKER) stop postgres
