import io
import sys
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import re

User = get_user_model()

@override_settings(EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend')
class SignupAndVerifyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create(
            username="authuser",
            email="authuser@example.com",
            phone_number="1234567890",
            password=make_password("authpassword123"),
            is_active=True
        )
        refresh = RefreshToken.for_user(self.test_user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self._stdout = sys.stdout
        self.output = io.StringIO()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = self._stdout

    def test_signup_success(self):
        payload = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "phone_number": "1234567890", 
            "is_gender": True, 
            "password": "testpassword123",
        }
        response = self.client.post('/api/signup/', payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"message": "Verification code sent to email. Check your console for the code."})
        
        user = User.objects.get(username="testuser")
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.email_code) 
        
        email_output = self.output.getvalue()
        self.assertIn("Your email verification code is:", email_output)
        code_match = re.search(r"Your email verification code is: (\d{6})", email_output)
        self.assertIsNotNone(code_match)
        stored_code = user.email_code
        self.assertEqual(code_match.group(1), stored_code)

    def test_verify_code_success(self):
        user = User.objects.create(
            username="verifyuser",
            first_name="Verify",
            last_name="User",
            email="verifyuser@example.com",
            phone_number="1234567890",
            password=make_password("verifyPassword123"),
            date_joined="2025-05-10T12:00:00Z",
            is_active=False,
            email_code="123456",
            is_gender=True
        )
        
        payload = {"email_code": "123456"}
        response = self.client.post('/api/verify-code/', payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Verification successful. You can now log in."})
        
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertIsNone(user.email_code)

    def test_verify_code_failure(self):
        user = User.objects.create(
            username="verifyfail",
            first_name="VerifyFail",
            last_name="User",
            email="verifyfail@example.com",
            phone_number="1234567890",
            password=make_password("verifyFail123"),
            date_joined="2025-05-10T12:00:00Z",
            is_active=False,
            email_code="123456"
        )
        
        payload = {"email_code": "654321"}
        response = self.client.post('/api/verify-code/', payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Invalid verification code."})
        
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        self.assertEqual(user.email_code, "123456") 