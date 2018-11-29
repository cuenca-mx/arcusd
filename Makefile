SHELL := bash
PYTHON=python3.7


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

travis-test:
		pip install -q pycodestyle
		$(MAKE) lint

.PHONY: install install-dev lint clean-pyc test
