#!/usr/bin/env bash -e

make clean-pyc
pip install -q --upgrade pip
make install-dev

make test

make code-coverage