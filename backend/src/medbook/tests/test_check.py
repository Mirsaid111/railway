import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from medbook.models import MedicalTest

User = get_user_model()

@pytest.mark.django_db
def test_protected_test_list_view():

    user = User.objects.create_user(username='testuser', password='testpass')
    MedicalTest.objects.create(name='Test 1')
    MedicalTest.objects.create(name='Test 2')

    client = APIClient()
    
    response = client.get('/api/medical-tests/')
    assert response.status_code in [401, 403], (
        "Unauthenticated requests should be rejected (401 or 403)"
    )

    client.force_authenticate(user=user)
    response = client.get('/api/medical-tests/')
    assert response.status_code == 200
    assert len(response.data) == 2 