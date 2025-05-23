
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Organization(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=255)

class AccessCode(models.Model):
    code = models.CharField(max_length=10)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

class Trainee(models.Model):
    phone_number = models.CharField(max_length=20)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, through='AccessGrant')

class AccessGrant(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    access_granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=lambda: timezone.now() + timedelta(days=730))

