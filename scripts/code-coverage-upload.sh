#!/usr/bin/env bash

make code-coverage
coveralls
make docker-stop
