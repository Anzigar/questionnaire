#!/bin/bash
set -e

# Debug: Check if pandas is imported in the export_service.py file
echo "Checking export_service.py for pandas imports..."
if grep -q "import pandas" /app/export_service.py; then
    echo "ERROR: export_service.py still contains pandas import!"
    echo "File content:"
    cat /app/export_service.py
    exit 1
else
    echo "export_service.py looks good - no pandas imports found"
fi

# Debug: List installed packages
echo "Installed Python packages:"
pip list

# Start the application
echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
