
alembic upgrade head

uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}
