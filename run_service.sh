#!/bin/sh

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Setup tasks
log "Running setup tasks..."

# Create proxy network if it doesn't exist
if ! docker network ls | grep -q "proxy"; then
    log "Creating Docker network 'proxy'..."
    docker network create proxy || log "Network might already exist or insufficient permissions"
fi

# Create and set permissions for acme.json if it doesn't exist
if [ ! -f "acme.json" ]; then
    log "Creating acme.json..."
    touch acme.json
    chmod 600 acme.json
    log "acme.json created with proper permissions"
fi

# Start the application
log "Starting the application..."

docker compose up --build -d