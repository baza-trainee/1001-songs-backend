#!/usr/bin/env bash

alembic upgrade head
python3 -m scripts.initial_db
gunicorn -c gunicorn.conf.py src.main:app
