#!/usr/bin/env bash
make install-dev

python scripts/create_mappings_for_test.py
pytest tests/ --cov=./ --cov-report=xml