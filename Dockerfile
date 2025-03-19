FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Explicitly install alembic to ensure it's available
RUN pip install alembic

COPY . .
RUN mkdir -p db
RUN chmod +x entrypoint.sh

# Use ARG to properly pass PORT during build if needed
ARG PORT=8000
ENV PORT=${PORT}
EXPOSE ${PORT}

ENTRYPOINT ["./entrypoint.sh"]