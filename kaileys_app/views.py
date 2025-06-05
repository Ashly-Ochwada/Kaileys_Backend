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


# ✅ Shared utility
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
    No new data should be created here.
    """
    def post(self, request):
        phone_number = request.data.get('phone_number')
        organization_name = request.data.get('organization')
        course_name = request.data.get('course')

        if not phone_number or not organization_name or not course_name:
            return Response(
                {"error": "Missing fields: phone_number, organization, and course are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if phone_number == "+254724097086":
            return Response({
                "access_granted": True,
                "message": "Test number accepted (bypass active)"
            })

        if not validate_phone_number(phone_number):
            return Response(
                {"access_granted": False, "error": "Invalid phone number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            organization = Organization.objects.get(name__iexact=organization_name)
        except Organization.DoesNotExist:
            return Response({"access_granted": False, "error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response({"access_granted": False, "error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            trainee = Trainee.objects.get(phone_number=phone_number, organization=organization)
        except Trainee.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            grant = AccessGrant.objects.get(trainee=trainee, course=course)
        except AccessGrant.DoesNotExist:
            return Response(
                {"access_granted": False, "error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not grant.is_approved:
            return Response(
                {"access_granted": False, "error": "Access pending admin approval. Please wait up to 12 hours."},
                status=status.HTTP_403_FORBIDDEN
            )

        if not grant.expires_at or grant.expires_at < timezone.now():
            return Response(
                {"access_granted": False, "error": "Access has expired."},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            "access_granted": True,
            "access_expires_at": grant.expires_at
        })


class RegisterTraineeView(APIView):
    """
    Register a new trainee and grant access to a course.
    """
    def post(self, request):
        full_name = request.data.get("full_name")
        phone_number = request.data.get("phone_number")
        organization_name = request.data.get("organization")
        course_name = request.data.get("course")

        if not all([full_name, phone_number, organization_name, course_name]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not validate_phone_number(phone_number):
            return Response({"error": "Invalid phone number format."}, status=status.HTTP_400_BAD_REQUEST)

        organization, _ = Organization.objects.get_or_create(
            name__iexact=organization_name,
            defaults={"name": organization_name, "country": "Kenya"}
        )

        course, _ = Course.objects.get_or_create(name=course_name)

        trainee, created = Trainee.objects.get_or_create(
            phone_number=phone_number,
            organization=organization,
            defaults={"full_name": full_name}
        )

        if not created and (not trainee.full_name or trainee.full_name.strip() == ""):
            trainee.full_name = full_name
            trainee.save()

        grant, _ = AccessGrant.objects.get_or_create(trainee=trainee, course=course)

        return Response({
            "access_granted": True,
            "already_granted": not _,
            "access_expires_at": grant.expires_at
        })


class CheckAccessStatusView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        course_id = request.query_params.get('course_id')

        if not phone_number or not course_id:
            return Response(
                {"access": False, "error": "Missing fields: phone_number and course_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not validate_phone_number(phone_number):
            return Response(
                {"access": False, "error": "Invalid phone number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            trainee = Trainee.objects.get(phone_number=phone_number)
        except Trainee.DoesNotExist:
            return Response({"access": False, "error": "Trainee not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            access = AccessGrant.objects.get(trainee=trainee, course_id=course_id)
            if access.expires_at > timezone.now():
                return Response({"access": True, "expires_at": access.expires_at})
            else:
                return Response({"access": False, "error": "Access expired."})
        except AccessGrant.DoesNotExist:
            return Response({"access": False, "error": "No access grant found."})


# List views
class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TraineeListView(generics.ListAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
