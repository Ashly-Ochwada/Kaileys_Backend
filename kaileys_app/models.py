from django.db import models
from django.utils import timezone
from datetime import timedelta
from .utils import generate_unique_code


# Utility function for default expiry (2 years)
def default_expiry():
    return timezone.now() + timedelta(days=730)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country})"


class Course(models.Model):
    from django.db.models import TextChoices

    class CourseChoices(TextChoices):
        FIRE_SAFETY = "fire_safety", "Fire Safety Training"
        FIRST_AID = "first_aid", "First Aid"
        SAFETY_COMMITTEE = "safety_committee", "Safety and Health Committee Training"

    name = models.CharField(
        max_length=100,
        choices=CourseChoices.choices,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return self.get_name_display()


class AccessCode(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @property
    def is_valid(self):
        return timezone.now() < self.expires_at

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} | {self.course.name} @ {self.organization.name}"


class Trainee(models.Model):
    phone_number = models.CharField(max_length=20, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, through='AccessGrant')

    class Meta:
        unique_together = ('phone_number', 'organization')

    def __str__(self):
        return f"{self.phone_number} ({self.organization.name})"


class AccessGrant(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    access_granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

    def __str__(self):
        return (
            f"Access: {self.trainee.phone_number} -> {self.course.name} "
            f"(expires: {self.expires_at.date()})"
        )
