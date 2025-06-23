import pytest
from rest_framework.test import APIClient
from .models import Resource # <--- DODAJEMY TEN IMPORT

@pytest.mark.django_db
def test_resource_list_returns_200():
    """
    Sprawdza, czy endpoint z listą zasobów jest dostępny i zwraca status 200 OK.
    """
    client = APIClient()
    response = client.get('/api/resources/')
    assert response.status_code == 200

# === DODAJ TEN NOWY TEST PONIŻEJ ===
@pytest.mark.django_db
def test_resource_list_returns_correct_number_of_items():
    """
    Sprawdza, czy API zwraca poprawną liczbę zasobów.
    """
    # Krok 1: Arrange - tworzymy dane testowe w tymczasowej bazie danych
    Resource.objects.create(name='Test Resource 1', capacity=5)
    Resource.objects.create(name='Test Resource 2', capacity=10)
    client = APIClient()

    # Krok 2: Act - wysyłamy żądanie
    response = client.get('/api/resources/')

    # Krok 3: Assert - sprawdzamy wyniki
    assert response.status_code == 200
    # Sprawdzamy, czy w odpowiedzi JSON jest lista zawierająca DOKŁADNIE 2 elementy
    assert len(response.data) == 2

# === DODAJ I TEN TEST ===
@pytest.mark.django_db
def test_resource_detail_returns_correct_data():
    """
    Sprawdza, czy API dla pojedynczego zasobu zwraca poprawne dane.
    """
    # Arrange - tworzymy jeden konkretny zasób
    resource = Resource.objects.create(name='Sala Testowa', capacity=15)
    client = APIClient()

    # Act - odpytujemy o szczegóły tego konkretnego zasobu
    response = client.get(f'/api/resources/{resource.id}/')

    # Assert - sprawdzamy, czy dane w odpowiedzi się zgadzają
    assert response.status_code == 200
    assert response.data['name'] == 'Sala Testowa'
    assert response.data['capacity'] == 15