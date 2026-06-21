from rest_framework import serializers
from .models import Organization, Course, Trainee


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'country']


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(choices=Course.CourseChoices.choices)

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'access_code',
            'access_code_expires_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = dict(
            Course.CourseChoices.choices
        ).get(representation['name'], representation['name'])
        return representation


class TraineeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    organization = OrganizationSerializer(read_only=True)

    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source='organization',
        write_only=True
    )

    class Meta:
        model = Trainee
        fields = [
            'id',
            'full_name',
            'phone_number',
            'organization',
            'organization_id'
        ]