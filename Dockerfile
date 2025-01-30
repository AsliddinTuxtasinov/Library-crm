FROM python:3.11-alpine as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app/backend

# Set the working directory in the container
WORKDIR /app/backend

# Install system dependencies
RUN apk update && \
    apk add --no-cache \
        gettext \
        postgresql-dev \
        gcc \
        python3-dev \
        musl-dev \
        libpq \
        build-base

# Copy the rest of the application
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run the application
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
