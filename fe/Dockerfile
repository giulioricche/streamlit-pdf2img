FROM python:3.11.8-slim

USER root
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN apt-get -y install curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

# Copy project structure
COPY pdf2imgfe/.streamlit/ ./pdf2imgfe/.streamlit/
COPY pdf2imgfe/lib/ ./pdf2imgfe/lib/
COPY pdf2imgfe/services/ ./pdf2imgfe/services/
COPY pdf2imgfe/app_components/ ./pdf2imgfe/app_components/
COPY pdf2imgfe/app.py ./pdf2imgfe/app.py

# Initialize Poetry
COPY ./pyproject.toml ./
RUN poetry install --no-interaction --no-ansi

# Expose application port
EXPOSE $FE_APP_PORT

# Start command
WORKDIR /app/pdf2imgfe
CMD poetry run streamlit run app.py --server.address 0.0.0.0 --server.port $FE_APP_PORT --server.baseUrlPath ${FE_BASE_URL_PATH}
