#!/bin/bash

# Script to run the SeaJobs application locally

echo "=== Running SeaJobs locally ==="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "=== Building the frontend application ==="
cd frontend
# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Build the frontend
echo "Building the frontend..."
npm run build

# Return to root directory
cd ..

# Creating necessary directories
mkdir -p frontend/build
mkdir -p backend/static
mkdir -p backend/media

echo "=== Starting Docker containers ==="
echo "This will start the following services:"
echo "- PostgreSQL database"
echo "- MinIO object storage"
echo "- Django backend"
echo "- React frontend"
echo "- Nginx web server"
echo ""
echo "The application will be available at: http://localhost:80"
echo "MinIO console will be available at: http://localhost:80/minio"

# Start Docker containers
docker-compose up --build

# Exit
echo "=== Application has been stopped ==="