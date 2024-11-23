# Use the slim Python image for efficiency
FROM python:3.11.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . /app/

# Expose the port your application will run on
EXPOSE ${PORT:-8000}

# Set up start script permissions
RUN chmod +x start.sh

# Run the application using your start.sh script
CMD ["./start.sh"]
