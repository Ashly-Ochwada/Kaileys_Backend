# yourapp/create_admin.py
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

def run():
    try:
        if not User.objects.filter(username='kaileys').exists():
            User.objects.create_superuser(
                username='kaileys',
                email='kaileys@gmail.com',
                password='kc2025'
            )
            print("✅ Superuser created!")
        else:
            print("ℹ️ Superuser already exists.")
    except IntegrityError:
        print("⚠️ Superuser creation failed — already exists or DB not ready.")
