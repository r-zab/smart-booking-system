import pytest
from rest_framework.test import APIClient
from .models import Resource

@pytest.mark.django_db
def test_resource_list_returns_200():
    client = APIClient()
    response = client.get('/api/resources/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_resource_list_returns_correct_number_of_items():
    Resource.objects.create(name='Test Resource 1', capacity=5)
    Resource.objects.create(name='Test Resource 2', capacity=10)
    client = APIClient()
    response = client.get('/api/resources/')
    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_resource_detail_returns_correct_data():
    resource = Resource.objects.create(name='Sala Testowa', capacity=15)
    client = APIClient()
    response = client.get(f'/api/resources/{resource.id}/')
    assert response.status_code == 200
    assert response.data['name'] == 'Sala Testowa'
    assert response.data['capacity'] == 15
