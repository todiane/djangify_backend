# Use Python 3.11 slim image
FROM python:3.11.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.7.1 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_NO_INTERACTION=1 \
  DJANGO_SETTINGS_MODULE=config.settings.production \
  PORT=8000

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  curl \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${POETRY_HOME}/bin:$PATH"

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-dev --no-root

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p staticfiles media/blog media/portfolio media/summernote \
  && chmod +x start.sh

# Expose port
EXPOSE 8000

# Set Python path
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Run the start script
CMD ["./start.sh"]
