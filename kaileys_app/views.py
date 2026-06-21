from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
import re

from .models import Organization, Course, Trainee
from .serializers import (
    OrganizationSerializer,
    CourseSerializer,
    TraineeSerializer,
)
from rest_framework.reverse import reverse


def validate_phone_number(phone_number: str) -> bool:
    phone_regex = r"^\+(254|256|250)\d{9}$"
    return bool(re.match(phone_regex, phone_number))


class APIRootView(APIView):
    def get(self, request, format=None):
        return Response({
            'verify-access': reverse('verify-access', request=request),
            'register-trainee': reverse('register-trainee', request=request),
            'organizations': reverse('organizations', request=request),
            'courses': reverse('courses', request=request),
            'trainees': reverse('trainees', request=request),
        })


class VerifyAccessView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        org_name = request.data.get('organization')
        course_name = request.data.get('course')
        access_code = request.data.get('access_code')

        if not all([phone, org_name, course_name, access_code]):
            return Response(
                {"access_granted": False, "error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not validate_phone_number(phone):
            return Response(
                {"access_granted": False, "error": "Invalid phone number format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        organization, _ = Organization.objects.get_or_create(
            name__iexact=org_name,
            defaults={"name": org_name, "country": "Kenya"}
        )

        trainee, _ = Trainee.objects.get_or_create(
            phone_number=phone,
            organization=organization
        )

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if course.access_code != access_code:
            return Response(
                {"access_granted": False, "error": "Invalid access code"},
                status=status.HTTP_403_FORBIDDEN
            )

        if course.access_code_expires_at < timezone.now():
            return Response(
                {"access_granted": False, "error": "Access code has expired"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            "access_granted": True,
            "message": "Access granted successfully",
            "course": course.get_name_display(),
            "access_code_expires_at": course.access_code_expires_at
        })


class RegisterTraineeView(APIView):
    def post(self, request):
        full_name = request.data.get("full_name")
        phone = request.data.get("phone_number")
        org_name = request.data.get("organization")
        course_name = request.data.get("course")
        access_code = request.data.get("access_code")

        if not all([full_name, phone, org_name, course_name, access_code]):
            return Response(
                {"access_granted": False, "error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not validate_phone_number(phone):
            return Response(
                {"access_granted": False, "error": "Invalid phone number format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        organization, _ = Organization.objects.get_or_create(
            name__iexact=org_name,
            defaults={"name": org_name, "country": "Kenya"}
        )

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if course.access_code != access_code:
            return Response(
                {"access_granted": False, "error": "Invalid access code"},
                status=status.HTTP_403_FORBIDDEN
            )

        if course.access_code_expires_at < timezone.now():
            return Response(
                {"access_granted": False, "error": "Access code has expired"},
                status=status.HTTP_403_FORBIDDEN
            )

        trainee, created = Trainee.objects.get_or_create(
            phone_number=phone,
            organization=organization,
            defaults={"full_name": full_name}
        )

        if not created and trainee.full_name != full_name:
            trainee.full_name = full_name
            trainee.save()

        return Response({
            "access_granted": True,
            "message": "Access granted successfully",
            "trainee_id": trainee.id,
            "course": course.get_name_display(),
            "access_code_expires_at": course.access_code_expires_at
        })


class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TraineeListView(generics.ListAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer