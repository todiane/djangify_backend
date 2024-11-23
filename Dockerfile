FROM python:3.11.10-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc \
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
  DJANGO_SETTINGS_MODULE=config.settings \
  PYTHONDONTWRITEBYTECODE=1 \
  PORT=8080

EXPOSE 8080

COPY start.sh /app/
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]
