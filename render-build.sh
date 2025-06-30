#!/usr/bin/env bash
set -o errexit   # exit on error
set -o pipefail
set -o nounset

echo "🚀 RUNNING render-build.sh"

echo "📦 Installing Python packages…"
pip install --no-cache-dir -r requirements.txt

echo "🗄️  Running migrations…"
python3 manage.py migrate --noinput

echo "🎨 Collecting static files…"
python3 manage.py collectstatic --noinput

# --------------------------------------------------
# Bullet-proof super-user creator (idempotent)
# --------------------------------------------------
if [[ "${CREATE_SUPERUSER:-false}" == "true" ]]; then
  python3 manage.py shell - <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username  = os.environ["DJANGO_SUPERUSER_USERNAME"]
email     = os.environ["DJANGO_SUPERUSER_EMAIL"]
password  = os.environ["DJANGO_SUPERUSER_PASSWORD"]

u, _ = User.objects.update_or_create(
        username=username,
        defaults={
            "email": email,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        })
u.set_password(password)
u.save()
print("✅ Super-user ready:", username)

# --- tiny sanity check ---
dump = list(User.objects.filter(is_superuser=True).values('username', 'is_staff'))
print("🔎 All super-users in DB ->", dump)
PY
fi