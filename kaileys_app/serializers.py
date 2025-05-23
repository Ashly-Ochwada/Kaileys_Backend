from rest_framework import serializers
from .models import Organization, Course, AccessCode, Trainee, AccessGrant

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'country']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description']


class AccessCodeSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = AccessCode
        fields = ['id', 'code', 'course', 'organization', 'created_at', 'expires_at']


class TraineeSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Trainee
        fields = ['id', 'phone_number', 'organization']


class AccessGrantSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = AccessGrant
        fields = ['id', 'trainee', 'course', 'access_granted_at', 'expires_at']
