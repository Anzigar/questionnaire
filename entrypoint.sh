#!/bin/bash
set -e

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
python -c "
import time
import pymysql
import os

db_host = os.getenv('DB_HOST', 'mysql')
db_port = int(os.getenv('DB_PORT', 3306))
db_user = os.getenv('DB_USER', 'questionnaire_user')
db_pass = os.getenv('DB_PASSWORD', 'questionnaire_password')
db_name = os.getenv('DB_NAME', 'questionnaire_db')

start_time = time.time()
while time.time() - start_time < 60:
    try:
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pass,
            database=db_name,
        )
        conn.close()
        print('Database connection successful!')
        break
    except pymysql.Error:
        print('Waiting for database connection...')
        time.sleep(3)
else:
    print('Database connection failed after 60 seconds!')
    exit(1)
"

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

# Create database tables if they don't exist
echo "Creating database tables if needed..."
python -c "from models import create_tables; create_tables()"

# Debug: List installed packages
echo "Installed Python packages:"
pip list

# Start the application
echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
