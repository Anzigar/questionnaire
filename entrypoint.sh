#!/bin/bash
set -e

# Wait for database if needed
# Uncomment and adjust if you're using a separate database container
# echo "Waiting for database to be ready..."
# while ! nc -z database 5432; do
#   sleep 0.1
# done

echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
