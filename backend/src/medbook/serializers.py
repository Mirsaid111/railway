from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.mail import send_mail
import random
import string
from .models import MedicalTest

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15, required=True)
    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'is_gender', 'date_joined', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_gender': {'required': True},
            'date_joined': {'read_only': True},
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['date_joined'] = timezone.now()
        validated_data['is_active'] = False
        email_code = ''.join(random.choices(string.digits, k=6))
        validated_data['email_code'] = email_code
        user = User.objects.create(**validated_data)
        send_mail(
            'Your Medbook Verification Code',
            f'Your email verification code is: {email_code}',
            'mir6raid@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return user

class VerifyCodeSerializer(serializers.Serializer):
    email_code = serializers.CharField(max_length=6)

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTest
        fields = ['id', 'name', 'age', 'created_at']