from rest_framework import serializers
from .models import Organization, Course, AccessCode, Trainee, AccessGrant

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'country']


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(choices=Course.CourseChoices.choices)

    class Meta:
        model = Course
        fields = ['id', 'name']

    def to_representation(self, instance):
        # Display the human-readable name in the response
        representation = super().to_representation(instance)
        representation['name'] = dict(Course.COURSE_CHOICES).get(representation['name'], representation['name'])
        return representation


class AccessCodeSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), source='organization', write_only=True
    )

    class Meta:
        model = AccessCode
        fields = ['id', 'code', 'course', 'course_id', 'organization', 'organization_id', 'created_at', 'expires_at']
        read_only_fields = ['code', 'created_at']  # Code is auto-generated


class TraineeSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), source='organization', write_only=True
    )

    class Meta:
        model = Trainee
        fields = ['id', 'phone_number', 'organization', 'organization_id']


class AccessGrantSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    trainee_id = serializers.PrimaryKeyRelatedField(
        queryset=Trainee.objects.all(), source='trainee', write_only=True
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = AccessGrant
        fields = ['id', 'trainee', 'trainee_id', 'course', 'course_id', 'access_granted_at', 'expires_at']
        read_only_fields = ['access_granted_at']
