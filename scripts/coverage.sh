#!/usr/bin/env bash
make install-dev

flask db upgrade

pytest tests/ --cov=./ --cov-report=xml