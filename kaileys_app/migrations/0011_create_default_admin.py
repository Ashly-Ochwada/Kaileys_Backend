# Generated by Django 5.1.5 on 2025-06-30 14:18

from django.db import migrations

import os
from django.contrib.auth import get_user_model
from django.db import migrations

def create_admin(apps, schema_editor):
    User = get_user_model()

    uname = os.getenv("DJANGO_SUPERUSER_USERNAME", "kaileysuser")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "kaileystraining@gmail.com")
    pwd   = os.getenv("DJANGO_SUPERUSER_PASSWORD")

    if not pwd:        # avoid committing a real hash to Git
        return

    user, created = User.objects.get_or_create(
        username=uname,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )
    if created:
        user.set_password(pwd)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('kaileys_app', '0010_alter_course_name'),
    ]

    operations = [
    ]
