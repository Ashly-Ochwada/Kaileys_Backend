import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta


def default_expiry():
    return timezone.now() + timedelta(days=730)


def default_code_expiry():
    return timezone.now() + timedelta(days=90)

class Organization(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country})"

from django.db import models

class Course(models.Model):
    from django.db.models import TextChoices

    class CourseChoices(TextChoices):
        FIRE_SAFETY = "fire_safety", "Fire Safety Training"
        FIRST_AID = "first_aid", "First Aid"
        SAFETY_COMMITTEE = "safety_committee", "Safety and Health Committee Training"
        CHEMICAL_SAFETY = "chemical_safety", "Chemical Safety"
        SCAFFOLDING_SAFETY = "scaffolding_safety", "Scaffolding, Ladder Safety and Work at Height Training"
        CONFINED_SPACE_SAFETY = "confined_space_safety", "Confined Space Safety"

    name = models.CharField(
        max_length=100,
        choices=CourseChoices.choices,
        unique=True,
        db_index=True
    )

    access_code = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        null=True
    )

    access_code_expires_at = models.DateTimeField(
        default=default_code_expiry
    )

    def save(self, *args, **kwargs):
        if not self.access_code:
            self.access_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()

class Trainee(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('phone_number', 'organization')

    def __str__(self):
        return f"{self.full_name} ({self.phone_number}, {self.organization.name})"