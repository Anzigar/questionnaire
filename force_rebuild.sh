#!/bin/bash
set -e

echo "Stopping and removing all containers..."
docker-compose down

echo "Removing Docker images for current project..."
docker-compose rm -f
docker rmi $(docker images -q questionnaire_questionnaire) || true

echo "Cleaning Docker system..."
docker system prune -f

echo "Rebuilding with no-cache option..."
docker-compose build --no-cache

echo "Starting services..."
docker-compose up -d

echo "Rebuild complete. Check logs with: docker-compose logs -f"
