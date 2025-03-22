#!/bin/sh

# Try to run alembic with full path
echo "Running database migrations..."
python -m alembic upgrade head || echo "Migration failed but continuing startup"
# Start the application
echo "Starting the application..."
uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}
