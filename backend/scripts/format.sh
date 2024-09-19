#! /usr/bin/env bash
set -e
set -x

black ./app --check
black ./app