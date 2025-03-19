#!/bin/sh

# Print debugging information
echo "Checking environment..."
echo "Python version: $(python --version)"
echo "PATH: $PATH"
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"
echo "Checking for alembic: $(which alembic 2>/dev/null || echo 'not found')"

# Try to run alembic with full path
echo "Running database migrations..."
python -m alembic upgrade head || echo "Migration failed but continuing startup"

# Start the application
echo "Starting the application..."
uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}
