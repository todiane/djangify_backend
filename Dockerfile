FROM python:3.11.10-slim AS builder

RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.11.10-slim

RUN apt-get update && apt-get install -y \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app .

RUN mkdir -p staticfiles static media/portfolio media/summernote

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

COPY start.sh /app/
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]