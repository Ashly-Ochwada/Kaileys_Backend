#!/usr/bin/env bash
set -o errexit

# Collect static files (skip if not using static)
python3 manage.py collectstatic --noinput

# Run database migrations
python3 manage.py migrate --noinput

# Create superuser only if the env variable is set
if [[ "$CREATE_SUPERUSER" == "true" ]]; then
  python3 manage.py createsuperuser \
    --no-input \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL" || true
fi