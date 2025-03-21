#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

echo "Running database migrations..."
python init_db.py

echo "Starting the application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 