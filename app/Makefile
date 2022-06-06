.PHONY: reqs requirements devreqs dev-requirements format check test coverage

RUNNER=

ifeq (${COMPOSE},1)
	RUNNER=docker-compose run --rm application
endif

BLACK=black --skip-string-normalization --line-length 79 --target-version py310

typecheck:
	python -m mypy --pretty --show-error-codes .

format_check:
	$(RUNNER) python -m isort . --only-sections --quiet --check-only --diff
	$(RUNNER) $(BLACK) --fast --check .

flake8:
	$(RUNNER) flake8 .

check: flake8 typecheck format_check


format:
	$(RUNNER) python -m isort . --only-sections
	$(RUNNER) $(BLACK) .

quicktest:
	$(RUNNER) python -m unittest $(DISCOVER) -v --catch $(TESTS)

pytest:
	$(RUNNER) coverage run -m unittest $(DISCOVER) --buffer --catch ${tests}

reqs requirements:
	$(RUNNER) pip install -r requirements.txt

devreqs dev-requirements:
	$(RUNNER) pip install -r requirements-dev.txt

test: check pytest

coverage: test
	$(RUNNER) coverage report

.PHONY: dev-server migrate migrations

ifndef DJANGO_HOST
	DJANGO_HOST=
endif

ifndef DJANGO_SETTINGS_MODULE
	export DJANGO_SETTINGS_MODULE=planeks_csv_generator.settings.local
endif

dev-server:
	$(RUNNER) python manage.py runserver $(DJANGO_HOST)

migrate:
	$(RUNNER) python manage.py migrate  --fake-initial

migrations:
	$(RUNNER) python manage.py migrate --fake-initial
	$(RUNNER) python manage.py loaddata api/*/fixtures/*.json
	$(RUNNER) python manage.py makemigrations --check --dry-run

check_migration:
	$(RUNNER) python local_manage.py sqlmigrate ${app} ${n}

# misc.
.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete -o -type d -name __pycache__ -delete
	rm -rf db[0-9]* api/static/ .mypy_cache/
