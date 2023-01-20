#!/bin/bash

/wait-for-it.sh db:5432 -t 60 --strict
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 80
