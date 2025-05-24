from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
import re
from .models import Organization, Course, AccessCode, Trainee, AccessGrant
from .serializers import (
    OrganizationSerializer,
    CourseSerializer,
    AccessCodeSerializer,
    TraineeSerializer,
    AccessGrantSerializer
)
from rest_framework.reverse import reverse

class APIRootView(APIView):
    """
    The API root listing all available endpoints.
    """
    def get(self, request, format=None):
        return Response({
            'verify-access': reverse('verify-access', request=request),
            'check-access': reverse('check-access', request=request),
            'generate-access-code': reverse('generate-access-code', request=request),
            'organizations': reverse('organizations', request=request),
            'courses': reverse('courses', request=request),
            'trainees': reverse('trainees', request=request),
        })

class VerifyAccessCodeView(APIView):
    """
    Trainee submits phone number and access code.
    If valid, grant access to the course with the same expiry as the access code.
    """
    def post(self, request):
        phone_number = request.data.get('phone_number')
        access_code = request.data.get('access_code')

        if not phone_number or not access_code:
            return Response(
                {"error": "Missing fields: phone_number and access_code are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate phone number
        if not self._validate_phone_number(phone_number):
            return Response(
                {"error": "Invalid phone number. Must be a valid Kenyan (+254), Ugandan (+256), or Rwandan (+250) number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find the access code
        try:
            access_code_obj = AccessCode.objects.get(code=access_code)
        except AccessCode.DoesNotExist:
            return Response({"error": "Invalid access code."}, status=status.HTTP_404_NOT_FOUND)

        if not access_code_obj.is_valid:
            return Response({"error": "Access code has expired."}, status=status.HTTP_403_FORBIDDEN)

        # Find or create the trainee
        trainee, created = Trainee.objects.get_or_create(
            phone_number=phone_number,
            defaults={'organization': access_code_obj.organization}
        )

        # Grant access if not already granted or update expiry
        grant, created = AccessGrant.objects.get_or_create(
            trainee=trainee,
            course=access_code_obj.course,
            defaults={'expires_at': access_code_obj.expires_at}
        )

        if not created:
            grant.expires_at = access_code_obj.expires_at
            grant.save()

        return Response({
            "access_granted": True,
            "already_granted": not created,
            "access_expires_at": grant.expires_at
        })

    def _validate_phone_number(self, phone_number: str) -> bool:
        """Validate phone number format for Kenyan, Ugandan, or Rwandan numbers."""
        phone_regex = r"^\+(254|256|250)\d{9}$"
        return bool(re.match(phone_regex, phone_number))

class CheckAccessStatusView(APIView):
    """
    Check if a trainee has access to a specific course.
    Uses GET with query parameters: phone_number and course_id.
    """
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        course_id = request.query_params.get('course_id')

        if not phone_number or not course_id:
            return Response(
                {"access": False, "error": "Missing fields: phone_number and course_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate phone number
        if not self._validate_phone_number(phone_number):
            return Response(
                {"access": False, "error": "Invalid phone number. Must be a valid Kenyan (+254), Ugandan (+256), or Rwandan (+250) number."},
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

    def _validate_phone_number(self, phone_number: str) -> bool:
        """Validate phone number format for Kenyan, Ugandan, or Rwandan numbers."""
        phone_regex = r"^\+(254|256|250)\d{9}$"
        return bool(re.match(phone_regex, phone_number))

class GenerateAccessCodeView(APIView):
    """
    Generate a new access code for an organization and course.
    Accepts organization_id, course_id, and optional days_valid (default 7).
    """
    def post(self, request):
        organization_id = request.data.get('organization_id')
        course_id = request.data.get('course_id')
        days_valid = request.data.get('days_valid', 7)

        if not organization_id or not course_id:
            return Response(
                {"error": "Missing fields: organization_id and course_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            organization = Organization.objects.get(id=organization_id)
            course = Course.objects.get(id=course_id)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        expires_at = timezone.now() + timedelta(days=int(days_valid))
        access_code = AccessCode.objects.create(
            course=course,
            organization=organization,
            expires_at=expires_at
        )

        serializer = AccessCodeSerializer(access_code)
        return Response(
            {"success": True, "access_code": serializer.data},
            status=status.HTTP_201_CREATED
        )

# Optional: standard list views for admin/test use
class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TraineeListView(generics.ListAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer