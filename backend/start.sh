#!/bin/bash
set -e

echo "======================================"
echo "Starting Patient Management System"
echo "======================================"

# Wait for database to be ready
echo "Waiting for database to be ready..."
max_retries=30
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if python -c "
import sys
import time
from sqlalchemy import create_engine, text
from app.core.config import settings

try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    print('Database is ready!')
    sys.exit(0)
except Exception as e:
    print(f'Database not ready yet: {e}')
    sys.exit(1)
" 2>/dev/null; then
        echo "✓ Database connection successful!"
        break
    else
        retry_count=$((retry_count + 1))
        echo "Attempt $retry_count/$max_retries - Database not ready yet..."
        sleep 2
    fi
done

if [ $retry_count -eq $max_retries ]; then
    echo "✗ Failed to connect to database after $max_retries attempts"
    exit 1
fi

# Run database initialization
echo ""
echo "Initializing database..."
python init_db.py

if [ $? -eq 0 ]; then
    echo "✓ Database initialized successfully!"
else
    echo "✗ Database initialization failed!"
    exit 1
fi

# Start the application
echo ""
echo "======================================"
echo "Starting FastAPI application..."
echo "======================================"
echo "API will be available at: http://localhost:8000"
echo "API Docs: http://localhost:8000/api/docs"
echo "======================================"
echo ""

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload