#!/bin/bash
set -e

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
python -c "



echo "Installed Python packages:"

pip list


echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
