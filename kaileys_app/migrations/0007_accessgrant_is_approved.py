# Generated by Django 5.2.1 on 2025-06-05 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaileys_app', '0006_trainee_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessgrant',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
