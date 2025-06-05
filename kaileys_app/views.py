from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
import re

from .models import Organization, Course, Trainee, AccessGrant
from .serializers import (
    OrganizationSerializer,
    CourseSerializer,
    TraineeSerializer,
    AccessGrantSerializer
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
            'check-access': reverse('check-access', request=request),
            'organizations': reverse('organizations', request=request),
            'courses': reverse('courses', request=request),
            'trainees': reverse('trainees', request=request),
        })

class VerifyAccessView(APIView):
    """
    Verify if a registered trainee has access to a course.
    Access is only granted if:
      - Trainee exists
      - Course exists
      - AccessGrant exists and is approved
      - Access is not expired
    """
    def post(self, request):
        phone = request.data.get('phone_number')
        org_name = request.data.get('organization')
        course_name = request.data.get('course')

        if not all([phone, org_name, course_name]):
            return Response(
                {"access_granted": False, "error": "Missing required fields: phone_number, organization, and course"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Test bypass for development
        if phone == "+254724097086":
            return Response({
                "access_granted": True,
                "message": "Test number accepted (bypass active)"
            })

        if not validate_phone_number(phone):
            return Response(
                {"access_granted": False, "error": "Invalid phone number format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            organization = Organization.objects.get(name__iexact=org_name)
        except Organization.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Organization not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            trainee = Trainee.objects.get(phone_number=phone, organization=organization)
        except Trainee.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Trainee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            grant = AccessGrant.objects.get(trainee=trainee, course=course)
        except AccessGrant.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Access not granted"},
                status=status.HTTP_404_NOT_FOUND
            )

   class VerifyAccessView(APIView):
    """
    Verify if a registered trainee has access to a course.
    Access is only granted if:
      - Trainee exists
      - Course exists
      - AccessGrant exists and is approved
      - Access is not expired
    """
    def post(self, request):
        phone = request.data.get('phone_number')
        org_name = request.data.get('organization')
        course_name = request.data.get('course')

        if not all([phone, org_name, course_name]):
            return Response(
                {"access_granted": False, "error": "Missing required fields: phone_number, organization, and course"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Test bypass for development
        if phone == "+254724097086":
            return Response({
                "access_granted": True,
                "message": "Test number accepted (bypass active)"
            })

        if not validate_phone_number(phone):
            return Response(
                {"access_granted": False, "error": "Invalid phone number format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            organization = Organization.objects.get(name__iexact=org_name)
        except Organization.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Organization not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            trainee = Trainee.objects.get(phone_number=phone, organization=organization)
        except Trainee.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Trainee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            grant = AccessGrant.objects.get(trainee=trainee, course=course)
        except AccessGrant.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "Access not granted"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Approval check before expiration
        if not grant.is_approved:
            return Response(
                {"access_granted": False, "error": "Access pending admin approval."},
                status=status.HTTP_403_FORBIDDEN
            )

        if not grant.expires_at or grant.expires_at < timezone.now():
            return Response(
                {"access_granted": False, "error": "Access has expired"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            "access_granted": True,
            "access_expires_at": grant.expires_at,
            "is_approved": grant.is_approved
        })
     # ✅ Approval check before expiration
        if not grant.is_approved:
            return Response(
                {"access_granted": False, "error": "Access pending admin approval."},
                status=status.HTTP_403_FORBIDDEN
            )

        if not grant.expires_at or grant.expires_at < timezone.now():
            return Response(
                {"access_granted": False, "error": "Access has expired"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            "access_granted": True,
            "access_expires_at": grant.expires_at,
            "is_approved": grant.is_approved
        })


class RegisterTraineeView(APIView):
    """
    Register a new trainee and grant access to a course.
    """
    def post(self, request):
        full_name = request.data.get("full_name")
        phone = request.data.get("phone_number")
        org_name = request.data.get("organization")
        course_name = request.data.get("course")

        if not all([full_name, phone, org_name, course_name]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not validate_phone_number(phone):
            return Response({"error": "Invalid phone number format"}, status=status.HTTP_400_BAD_REQUEST)

        organization, _ = Organization.objects.get_or_create(
            name__iexact=org_name,
            defaults={"name": org_name, "country": "Kenya"}
        )

        course, _ = Course.objects.get_or_create(name=course_name)

        trainee, created = Trainee.objects.get_or_create(
            phone_number=phone,
            organization=organization,
            defaults={"full_name": full_name}
        )

        if not created and (not trainee.full_name or trainee.full_name.strip() == ""):
            trainee.full_name = full_name
            trainee.save()

        grant, grant_created = AccessGrant.objects.get_or_create(
            trainee=trainee,
            course=course
        )

        return Response({
            "access_granted": True,
            "already_granted": not grant_created,
            "access_expires_at": grant.expires_at
        })


class CheckAccessStatusView(APIView):
    """
    Check if a user still has valid access for a specific course.
    """
    def get(self, request):
        phone = request.query_params.get('phone_number')
        course_id = request.query_params.get('course_id')

        if not phone or not course_id:
            return Response(
                {"access": False, "error": "Missing phone_number or course_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not validate_phone_number(phone):
            return Response(
                {"access": False, "error": "Invalid phone number format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            trainee = Trainee.objects.get(phone_number=phone)
        except Trainee.DoesNotExist:
            return Response({"access": False, "error": "Trainee not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            grant = AccessGrant.objects.get(trainee=trainee, course_id=course_id)
            if grant.expires_at > timezone.now():
                return Response({"access": True, "expires_at": grant.expires_at})
            else:
                return Response({"access": False, "error": "Access expired"})
        except AccessGrant.DoesNotExist:
            return Response({"access": False, "error": "Access grant not found"})


# List endpoints
class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TraineeListView(generics.ListAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
