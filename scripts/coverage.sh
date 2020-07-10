#!/usr/bin/env bash
make install-dev

pytest tests/ --cov=./ --cov-report=xml