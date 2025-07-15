FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file if it exists
COPY requirements.txt* ./

# Install Python dependencies
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy application code
COPY . .

# Expose port for development server
EXPOSE 8000

# Default command
CMD ["supervisord", "-c", "supervisord.conf"]
