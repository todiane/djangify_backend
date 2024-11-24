# Use the official Python image as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ensure migrations don't hang by enabling a timeout for the Docker container
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl --fail http://localhost:${PORT:-8080} || exit 1

# Expose port
EXPOSE 8080

# Run the entrypoint script
CMD ["./start.sh"]
