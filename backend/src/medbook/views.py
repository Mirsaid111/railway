from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, VerifyCodeSerializer, TestSerializer
from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import MedicalTest
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Доступ разрешен!"})

class SomeProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Это защищенный эндпоинт"})

class TestListView(generics.ListAPIView):
    queryset = MedicalTest.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Это защищенный эндпоинт",
            "data": serializer.data
        })

class SignupView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'first_name', 'last_name', 'email', 'phone_number', 'is_gender', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for the user'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name of the user'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name of the user'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Email address of the user'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number of the user (e.g., +998901234567)'),
                'is_gender': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Gender of the user (true for male, false for female)'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the user account'),
            },
        ),
        responses={
            201: openapi.Response(
                description="Verification code sent",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Invalid input",
        },
        operation_description="Register a new user with required fields. A verification code will be sent to the email."
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Verification code sent to email. Check your console for the code."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email_code'],
            properties={
                'email_code': openapi.Schema(type=openapi.TYPE_STRING, description='6-digit verification code sent to email'),
            },
        ),
        responses={
            200: openapi.Response(
                description="Verification successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Invalid code or input",
        },
        operation_description="Verify user by submitting the email verification code."
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            email_code = serializer.validated_data['email_code']
            try:
                user = User.objects.get(email_code=email_code)
                if not user.is_active:
                    user.is_active = True
                    user.email_code = None
                    user.save()
                    return Response({"message": "Verification successful. You can now log in."}, status=status.HTTP_200_OK)
                return Response({"message": "Account already verified."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)