FROM python:3.11.8-slim

USER root
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN apt-get -y install curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"
RUN apt-get -y install poppler-utils

# Copy project structure
COPY pdf2imgbe/lib/ ./pdf2imgbe/lib/
COPY pdf2imgbe/services/ ./pdf2imgbe/services/
COPY pdf2imgbe/app.py ./pdf2imgbe/app.py

# Initialize Poetry
COPY ./pyproject.toml ./
RUN poetry install --no-interaction --no-ansi

# Expose application port
EXPOSE $BE_APP_PORT

# Start command
WORKDIR /app/pdf2imgbe
CMD poetry run uvicorn app:app --host 0.0.0.0 --port $BE_APP_PORT
