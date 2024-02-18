#!/bin/bash
yes | poetry run alembic upgrade head
poetry run uvicorn main:app
