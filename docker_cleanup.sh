#!/bin/bash

echo "Stopping current containers..."
docker compose down

echo "Removing all stopped containers, unused networks, dangling images, and build cache..."
docker system prune -f

echo "Removing all unused images (not just dangling ones)..."
docker system prune -a -f

echo "Clearing build cache..."
docker builder prune -f


docker network create proxy || echo "Network 'proxy' already exists."

echo "Cache cleared. Rebuild and restart your containers with:"
echo "docker compose up --build -d"

docker compose up  -d
