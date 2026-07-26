# Stage 1: Builder
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build-time dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Final Image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Create a non-root user
RUN addgroup --system app && adduser --system --group app appuser
USER appuser

# Copy virtual environment and application code
COPY --from=builder /opt/venv /opt/venv
COPY app ./app

# Make the virtual environment active
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE ${PORT}

# Ensure permissions and run the application using the PORT environment variable
RUN chown -R appuser:app /opt/venv /app || true
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]

