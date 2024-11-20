# Build stage
FROM python:3.11.10-slim as builder

# Install Poetry and system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to create venv in project directory
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy project files
COPY . .

# Production stage
FROM python:3.11.10-slim

# Install PostgreSQL client
RUN apt-get update && apt-get install -y \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies and project files from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app .

# Create necessary directories
RUN mkdir -p staticfiles static media/portfolio media/summernote

# Only set non-sensitive environment variable
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

COPY start.sh /app/
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]
