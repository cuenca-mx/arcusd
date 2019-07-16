#!/usr/bin/env bash

make install-dev
python scripts/init_service_providers_mapping.py
make test