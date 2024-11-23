FROM python:3.11.10-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
  && pip install gunicorn

COPY . .

# Second stage
FROM python:3.11.10-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
  libpq-dev \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python packages and executables
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/
COPY --from=builder /app .

# Create necessary directories
RUN mkdir -p staticfiles static media/portfolio media/summernote \
  && mkdir -p apps/*/migrations \
  && find apps/*/migrations -type d -exec touch {}/__init__.py \;

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  DOCKER_CONTAINER=true \
  DEBUG=False \
  PORT=8080 \
  HOST=0.0.0.0

# Explicitly expose port 8080
EXPOSE 8080

# Create and set up start script
RUN echo '#!/bin/bash\n\
  set -e\n\
  \n\
  # Wait for PostgreSQL\n\
  if [ -n "$DATABASE_HOST" ]; then\n\
  echo "Waiting for PostgreSQL..."\n\
  while ! nc -z $DATABASE_HOST ${DATABASE_PORT:-5432}; do\n\
  sleep 1\n\
  done\n\
  echo "PostgreSQL is up"\n\
  fi\n\
  \n\
  python manage.py migrate --noinput\n\
  python manage.py collectstatic --noinput\n\
  \n\
  exec gunicorn config.wsgi:application \\\n\
  --bind 0.0.0.0:${PORT:-8080} \\\n\
  --workers 2 \\\n\
  --threads 2 \\\n\
  --timeout 120 \\\n\
  --access-logfile - \\\n\
  --error-logfile - \\\n\
  --log-level info' > /app/start.sh \
  && chmod +x /app/start.sh

ENTRYPOINT ["/app/start.sh"]
