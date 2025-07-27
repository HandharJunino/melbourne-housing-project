# Use Python 3.11 for Airflow compatibility (if needed)
FROM python:3.11-slim

# Use Python 3.12 to match your local environment (Airflow not supported)
# FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .

# Upgrade pip first to avoid installation issues
RUN pip install --upgrade pip

# Install dependencies with constraints to avoid conflicts
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p data/cleaned data/raw models visualisations

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose port (if you plan to add a web interface later)
EXPOSE 8000

# Default command
CMD ["python", "scripts/train_model.py"]