from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
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
            'organizations': reverse('organizations', request=request),
            'courses': reverse('courses', request=request),
            'trainees': reverse('trainees', request=request),
        })


class VerifyAccessCodeView(APIView):
    """
    Trainee submits phone number and access code.
    If valid, grant access to the course for 2 years.
    """

    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('access_code')

        try:
            access_code = AccessCode.objects.get(code=code)
        except AccessCode.DoesNotExist:
            return Response({"error": "Invalid access code."}, status=status.HTTP_404_NOT_FOUND)

        if not access_code.is_valid():
            return Response({"error": "Access code has expired."}, status=status.HTTP_403_FORBIDDEN)

        try:
            trainee = Trainee.objects.get(phone_number=phone, organization=access_code.organization)
        except Trainee.DoesNotExist:
            return Response({"error": "Trainee not found in the specified organization."}, status=status.HTTP_404_NOT_FOUND)

        # Grant access if not already granted
        grant, created = AccessGrant.objects.get_or_create(
            trainee=trainee,
            course=access_code.course,
            defaults={
                "expires_at": timezone.now() + timedelta(days=730)
            }
        )

        return Response({
            "access_granted": True,
            "already_granted": not created,
            "access_expires_at": grant.expires_at
        })


class CheckAccessStatusView(APIView):
    """
    Check if a trainee has access to a specific course
    """

    def get(self, request):
        phone = request.query_params.get('phone_number')
        course_id = request.query_params.get('course_id')

        try:
            trainee = Trainee.objects.get(phone_number=phone)
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
