from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, null=False, blank=False)  # Required field
    email_code = models.CharField(max_length=6, null=True, blank=True)  # For email verification
    is_active = models.BooleanField(default=False)
    is_gender = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class MedicalTest(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name