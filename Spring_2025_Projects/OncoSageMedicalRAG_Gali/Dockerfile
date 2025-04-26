# Multi-stage build for Medical-RAG application
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Create non-root user for security
RUN useradd -m appuser && \
    mkdir -p /app /home/appuser/.cache && \
    chown -R appuser:appuser /app /home/appuser/.cache

# Copy wheels from builder stage
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY --chown=appuser:appuser . .

# Copy entrypoint script
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_ENABLE_FILE_WATCHER=false \
    TOKENIZERS_PARALLELISM=false

# Switch to non-root user
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
