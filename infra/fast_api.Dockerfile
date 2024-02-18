FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY poetry.lock pyproject.toml ./

COPY app ./app

RUN poetry install --without dev

CMD ["poetry", "run", "uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
