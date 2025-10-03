# https://www.docker.com/blog/how-to-dockerize-django-app/

# STAGE 1 : Base build stage

FROM python:3.13-slim AS builder

# Create the app directory
RUN mkdir /app
WORKDIR /app

# Set environment variables to optimize Python
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# !! Libs système nécessaires pour compiler psycopg (non-binary)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Pip upgrade and install
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# STAGE 2 : Production stage
FROM python:3.13-slim

# !! Lib runtime nécessaire pour psycopg
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -m -r appuser && mkdir /app && chown -R appuser /app

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set working directory + copy code
WORKDIR /app
COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Staticfile
# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi:application"]
