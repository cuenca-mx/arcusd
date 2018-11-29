SHELL := bash
DOCKER=docker-compose run --rm arcusd
PYTHON=python3.6


install:
		pip install -q -r requirements.txt

install-dev: install
		pip install -q -r requirements-dev.txt

venv:
		$(PYTHON) -m venv --prompt arcusd venv
		source venv/bin/activate
		pip install --quiet --upgrade pip

lint:
		pycodestyle arcusd/ tests/

clean-pyc:
		find . -name '__pycache__' -exec rm -r "{}" +
		find . -name '*.pyc' -delete
		find . -name '*~' -delete

test: clean-pyc lint
		pytest

code-coverage:
		pip install coveralls
		coverage run --source arcusd -m py.test
		coverage report -m
		coveralls

travis-test:
		pip install -q pycodestyle
		$(MAKE) lint
		$(MAKE) docker-build
		$(DOCKER) scripts/test.sh
		$(MAKE) docker-stop

docker-test: docker-build
		# Clean up even if there's an error
		$(DOCKER) scripts/test.sh || $(MAKE) docker-stop
		$(MAKE) docker-stop

docker-build: clean-pyc
		docker-compose build
		touch docker-build

docker-stop:
		docker-compose stop
		docker-compose rm -f

clean-docker:
		docker-compose down --rmi local
		rm docker-build

docker-shell: docker-build
		# Clean up even if there's an error
		$(DOCKER) scripts/devwrapper.sh bash || $(MAKE) docker-stop
		$(MAKE) docker-stop



.PHONY: install install-dev lint clean-pyc test travis-test docker-test clean-docker docker-shell