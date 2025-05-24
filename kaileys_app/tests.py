from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from .models import Organization, Course, AccessCode, Trainee, AccessGrant
from .views import GenerateAccessCodeView

# Create a test client instance for making API requests
client = Client()

class AccessCodeModelTests(TestCase):
    """
    Test cases for the AccessCode model to ensure proper creation and validation.
    """

    def setUp(self):
        """
        Set up initial test data for each test method.
        Creates an organization, course, and an access code.
        """
        self.organization = Organization.objects.create(name="TestOrg", country="Kenya")
        self.course = Course.objects.create(name="fire_safety")
        self.access_code = AccessCode.objects.create(
            code="TEST1234",
            course=self.course,
            organization=self.organization,
            expires_at=timezone.now() + timedelta(days=7)
        )

    def test_code_uniqueness(self):
        """
        Test that creating an AccessCode with an existing code raises an IntegrityError.
        """
        with self.assertRaises(Exception):
            AccessCode.objects.create(
                code="TEST1234",
                course=self.course,
                organization=self.organization,
                expires_at=timezone.now() + timedelta(days=7)
            )

    def test_is_valid(self):
        """
        Test the is_valid method returns True for a non-expired code.
        """
        self.assertTrue(self.access_code.is_valid())

    def test_is_not_valid(self):
        """
        Test the is_valid method returns False for an expired code.
        """
        self.access_code.expires_at = timezone.now() - timedelta(days=1)
        self.access_code.save()
        self.assertFalse(self.access_code.is_valid())

class AccessCodeViewTests(TestCase):
    """
    Test cases for API views related to access codes.
    """

    def setUp(self):
        """
        Set up initial test data and URLs for each test method.
        Creates an organization, course, trainee, and access code.
        """
        self.organization = Organization.objects.create(name="TestOrg", country="Kenya")
        self.course = Course.objects.create(name="fire_safety")
        self.trainee = Trainee.objects.create(phone_number="+254712345678", organization=self.organization)
        self.access_code = AccessCode.objects.create(
            code="TEST5678",
            course=self.course,
            organization=self.organization,
            expires_at=timezone.now() + timedelta(days=7)
        )
        self.verify_url = reverse('verify-access')
        self.check_url = reverse('check-access')
        self.generate_url = reverse('generate-access-code')

    def test_verify_access_code_valid(self):
        """
        Test verifying a valid access code grants access to a trainee.
        """
        response = client.post(self.verify_url, {"phone_number": "+254712345678", "access_code": "TEST5678"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["access_granted"], True)

    def test_verify_access_code_invalid(self):
        """
        Test verifying an invalid access code returns a 404 error.
        """
        response = client.post(self.verify_url, {"phone_number": "+254712345678", "access_code": "INVALID"}, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Invalid access code.")

    def test_verify_access_code_expired(self):
        """
        Test verifying an expired access code returns a 403 error.
        """
        self.access_code.expires_at = timezone.now() - timedelta(days=1)
        self.access_code.save()
        response = client.post(self.verify_url, {"phone_number": "+254712345678", "access_code": "TEST5678"}, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["error"], "Access code has expired.")

    def test_verify_access_code_missing_fields(self):
        """
        Test verifying with missing fields returns a 400 error.
        """
        response = client.post(self.verify_url, {"phone_number": "+254712345678"}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Missing fields: phone_number and access_code are required")

    def test_check_access_status_valid(self):
        """
        Test checking access status for a valid grant returns 200 with access True.
        """
        AccessGrant.objects.create(trainee=self.trainee, course=self.course, expires_at=timezone.now() + timedelta(days=7))
        response = client.get(self.check_url, {"phone_number": "+254712345678", "course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["access"], True)

    def test_check_access_status_expired(self):
        """
        Test checking access status for an expired grant returns 200 with access False.
        """
        AccessGrant.objects.create(trainee=self.trainee, course=self.course, expires_at=timezone.now() - timedelta(days=1))
        response = client.get(self.check_url, {"phone_number": "+254712345678", "course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["access"], False)
        self.assertEqual(response.json()["error"], "Access expired.")

    def test_check_access_status_no_grant(self):
        """
        Test checking access status with no grant returns 200 with access False.
        """
        response = client.get(self.check_url, {"phone_number": "+254712345678", "course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["access"], False)
        self.assertEqual(response.json()["error"], "No access grant found.")

    def test_check_access_status_missing_fields(self):
        """
        Test checking access status with missing fields returns a 400 error.
        """
        response = client.get(self.check_url, {"phone_number": "+254712345678"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Missing fields: phone_number and course_id are required")

    def test_generate_access_code_valid(self):
        """
        Test generating a new access code returns a 201 with a unique code.
        """
        data = {"organization_id": self.organization.id, "course_id": self.course.id, "days_valid": 7}
        response = client.post(self.generate_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["success"])
        self.assertIn("access_code", response.json())
        self.assertEqual(len(response.json()["access_code"]["code"]), 8)  # Assuming 8-character code from utils.py

    def test_generate_access_code_missing_fields(self):
        """
        Test generating an access code with missing fields returns a 400 error.
        """
        response = client.post(self.generate_url, {"organization_id": self.organization.id}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Missing fields: organization_id and course_id are required")

    def test_generate_access_code_invalid_organization(self):
        """
        Test generating an access code with an invalid organization returns a 404 error.
        """
        data = {"organization_id": 999, "course_id": self.course.id, "days_valid": 7}
        response = client.post(self.generate_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Organization not found.")