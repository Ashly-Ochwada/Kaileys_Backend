#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset

echo "📦 Installing Python packages…"
pip install --no-cache-dir -r requirements.txt

echo "🗄️  Running migrations…"
python3 manage.py migrate --noinput

# 👑 Super‑user bootstrap (runs only when CREATE_SUPERUSER=True)
if [[ "${CREATE_SUPERUSER:-}" == "True" ]]; then
  echo "👑  Creating Django superuser…"
  python3 manage.py createsuperuser --no-input || true
fi
