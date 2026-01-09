FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy initialization script
COPY init_db.py .
COPY start.sh .

# Make startup script executable
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Run the application with initialization
CMD ["/app/start.sh"]