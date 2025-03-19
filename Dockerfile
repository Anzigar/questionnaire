FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create uploads directory
RUN mkdir -p uploads && chmod 777 uploads

# Copy entrypoint script and set permissions explicitly
COPY --chmod=755 entrypoint.sh .
# Double check permissions to ensure script is executable
RUN ls -la entrypoint.sh && \
    chmod +x entrypoint.sh && \
    echo "Permissions set correctly"

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
