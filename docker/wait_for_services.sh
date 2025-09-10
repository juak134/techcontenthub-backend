#!/usr/bin/env bash
set -e

host="${POSTGRES_HOST:-db}"; port="${POSTGRES_PORT:-5432}"
echo "Waiting for Postgres at $host:$port..."
until nc -z "$host" "$port"; do sleep 1; done
echo "Postgres is up."

# Small grace period for Elasticsearch
echo "Waiting a moment for Elasticsearch..."; sleep 5

# Make migrations for core (first run) and migrate
python manage.py makemigrations core --noinput || true
python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

exec "$@"
