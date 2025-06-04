from django.db import models
from django.utils import timezone
from datetime import timedelta

# Default expiry of 2 years for access grants
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

class Trainee(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True) 
    phone_number = models.CharField(max_length=20, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, through='AccessGrant')

    class Meta:
        unique_together = ('phone_number', 'organization')

    def __str__(self):
        return f"{self.full_name} ({self.phone_number}, {self.organization.name})"

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
