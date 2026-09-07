FROM python:3.12-slim

# Prevent Python from writing bytecode (.pyc) and ensure unbuffered stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DBT_PROFILES_DIR=/app

# Install minimal build tools required for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirement manifests first to leverage Docker layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project code
COPY . .

# Default command executes the full 5-step pipeline
CMD ["python", "orchestrator.py"]