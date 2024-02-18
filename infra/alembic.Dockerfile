FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY poetry.lock pyproject.toml alembic.ini ./

COPY alembic ./alembic
COPY app ./app

RUN poetry install --without dev

CMD ["poetry", "run", "alembic", "upgrade", "head"]
