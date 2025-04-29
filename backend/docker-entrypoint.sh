#!/bin/bash

set -e

# Wait for postgres
echo "Waiting for PostgreSQL..."
# Try to connect to PostgreSQL with a timeout of 60 seconds
timeout=60
counter=0
until nc -z $POSTGRES_HOST $POSTGRES_PORT || [ $counter -eq $timeout ]
do
  echo "PostgreSQL is unavailable - sleeping"
  counter=$((counter+1))
  sleep 1
done

if [ $counter -eq $timeout ]; then
  echo "Error: Timed out waiting for PostgreSQL to start"
  exit 1
fi

echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations..."
# Сначала мигрируем только accounts (пользователи), чтобы создать таблицу accounts_user
echo "Step 1: Migrating accounts app..."
python manage.py migrate accounts

# Затем мигрируем auth и остальные базовые приложения
echo "Step 2: Migrating auth and core apps..."
python manage.py migrate auth
python manage.py migrate admin
python manage.py migrate contenttypes
python manage.py migrate sessions
python manage.py migrate sites

# Затем мигрируем остальные приложения
echo "Step 3: Migrating other apps..."
python manage.py migrate

# Create superuser if not exists
echo "Creating superuser if not exists..."
python manage.py create_superuser_if_not_exists

# Collect static files
echo "Collecting static files..."
# Принудительно собираем статические файлы, включая файлы из drf-spectacular-sidecar
python manage.py collectstatic --no-input --clear

# Проверяем наличие статических файлов для Swagger UI
echo "Checking Swagger UI static files..."
if [ -d "/app/static/drf_spectacular_sidecar" ]; then
    echo "✅ Swagger UI static files found"
    ls -la /app/static/drf_spectacular_sidecar
else
    echo "❌ Swagger UI static files not found!"
    echo "Listing static directory:"
    ls -la /app/static/
fi

# Устанавливаем правильные права доступа на статические файлы
echo "Setting permissions on static files..."
chmod -R 755 /app/static/

# Initialize MinIO bucket
echo "Initializing MinIO bucket..."
python init_minio.py

# Start server
echo "Starting server..."
exec gunicorn seajobs.wsgi:application --bind 0.0.0.0:8000