FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./

RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY backend ./backend

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8080"]
