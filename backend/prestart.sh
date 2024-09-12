#! /usr/bin/env bash

# Let the DB start
python /app/app/pre_start.py

# Run migrations
alembic upgrade head
