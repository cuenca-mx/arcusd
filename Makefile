SHELL := bash
DOCKER=docker-compose run --rm arcusd
PYTHON=python3.8
PROJECT=arcusd
isort = isort $(PROJECT) tests setup.py
black = black -S -l 79 --target-version py37 $(PROJECT) tests setup.py

install:
		pip install -q -r requirements.txt

install-dev: install
		pip install -q -r requirements-dev.txt

venv:
		$(PYTHON) -m venv --prompt arcusd venv
		source venv/bin/activate
		pip install --quiet --upgrade pip

format:
		$(isort)
		$(black)

lint:
		$(isort) --check-only
		$(black) --check
		flake8 $(PROJECT) tests setup.py


test: clean-pyc lint
		python scripts/create_mappings_for_test.py
		pytest --cov-report=xml

docker-build: clean-pyc
		docker-compose build
		touch docker-build

docker-shell: docker-build
		# Clean up even if there's an error
		$(DOCKER) scripts/devwrapper.sh bash || $(MAKE) docker-stop
		$(MAKE) docker-stop

github-test: docker-build
		$(DOCKER) scripts/test.sh

github-coverage: docker-build
		$(DOCKER) scripts/coverage.sh

docker-stop:
		docker-compose stop
		docker-compose rm -f

clean: clean-docker clean-pyc

clean-pyc:
		find . -name '__pycache__' -exec rm -r "{}" +
		find . -name '*.pyc' -delete
		find . -name '*~' -delete

clean-docker:
		docker-compose down --rmi local
		rm docker-build


.PHONY: install install-dev lint clean-pyc test clean-docker docker-shell
