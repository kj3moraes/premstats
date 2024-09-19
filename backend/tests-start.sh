#! /usr/bin/env bash
set -e
set -x

# Do pre-test start up tasks 
python /app/app/tests_pre_start.py

# Run the tests
bash /app/scripts/test.sh "$@"
