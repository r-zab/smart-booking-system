# Inteligentny System Rezerwacji Zasobów (AI-Powered Booking System) - Backend

![Python](https://img.shields.io/badge/python-3.13-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-5.2-green.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-enabled-blue.svg?style=for-the-badge&logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg?style=for-the-badge)

Zaawansowany system backendowy do rezerwacji zasobów firmowych, zbudowany w **Django** i **Django REST Framework**.
Aplikacja udostępnia w pełni funkcjonalne **REST API** i jest wzbogacona o moduły sztucznej inteligencji do predykcji
zapotrzebowania oraz interakcji z użytkownikiem w języku naturalnym.

Całość jest w pełni **skonteneryzowana przy użyciu Dockera**, co zapewnia spójność środowiska i łatwość wdrożenia.

---
**Link do repozytorium frontendu:** [smart-booking-frontend (Vue.js UI)](https://github.com/r-zab/smart-booking-frontend)

---
## O Projekcie

Celem tego projektu było stworzenie solidnego i skalowalnego systemu backendowego, który odzwierciedla realne wyzwania
biznesowe. Aplikacja nie jest prostym CRUD-em – implementuje zaawansowaną logikę walidacji, zabezpieczenia oparte na
uwierzytelnianiu tokenowym oraz dwa odrębne moduły AI, demonstrując umiejętności wykraczające poza podstawy web
developmentu.

## Kluczowe Funkcjonalności

* **REST API:**
    * Pełna obsługa CRUD dla zasobów i rezerwacji za pomocą `ModelViewSet`.
    * Zaawansowane, zagnieżdżone serializery dla czytelnych i użytecznych odpowiedzi JSON.
    * Niestandardowe endpointy dla logiki biznesowej (np. `/api/resources/{id}/schedule/` do pobierania harmonogramu).
    * Endpoint do tworzenia użytkowników i autoryzacji opartej o tokeny.

* **Logika Biznesowa i Bezpieczeństwo:**
    * Zaawansowana walidacja w serializerze, zapobiegająca tworzeniu rezerwacji w zajętych już terminach.
    * Automatyczne przypisywanie rezerwacji do zalogowanego użytkownika (`request.user`) podczas jej tworzenia.
    * Wszystkie kluczowe endpointy zabezpieczone – dostępne tylko dla uwierzytelnionych użytkowników.
    * Filtrowanie wyników na poziomie API – użytkownicy widzą tylko swoje własne rezerwacje.

* **Moduł Predykcyjny (AI):**
    * Endpoint `/api/analytics/demand_prediction/` analizuje dane historyczne.
    * Wykorzystuje prosty model regresji liniowej (`scikit-learn`) do prognozowania zapotrzebowania na rezerwacje w
      przyszłości.

* **Inteligentny Asystent (Chatbot AI):**
    * Endpoint `/api/chatbot/` do interakcji w języku naturalnym.
    * Wykorzystuje logikę dopasowywania słów kluczowych i wyspecjalizowaną bibliotekę `dateparser` do rozumienia zapytań
      użytkownika o dostępność zasobów w konkretnym dniu i godzinie.

* **Narzędzia Deweloperskie:**
    * Dwa niestandardowe polecenia zarządzania (`seed_resources` i `seed_data`) do szybkiego wypełniania bazy danych
      danymi testowymi.
    * Zestaw testów automatycznych (`pytest`) weryfikujących działanie kluczowych endpointów API.

---

## Stos Technologiczny i Architektura

* **Backend:** Python, Django, Django REST Framework
* **Baza Danych:** PostgreSQL (uruchomiona w kontenerze Docker)
* **AI / Analiza Danych:** Pandas, Scikit-learn, dateparser
* **Konteneryzacja:** Docker, Docker Compose
* **Testowanie:** Pytest, pytest-django

Architektura systemu składa się z dwóch głównych kontenerów zarządzanych przez `docker-compose`: serwisu `app` z
aplikacją Django oraz serwisu `db` z bazą danych PostgreSQL, które komunikują się ze sobą w izolowanej sieci wirtualnej.

---

## Jak Uruchomić Projekt

Dzięki konteneryzacji, uruchomienie projektu jest niezwykle proste.

### Wymagania Wstępne

* Zainstalowany [Git](https://git-scm.com/)
* Zainstalowany [Docker](https://www.docker.com/products/docker-desktop/) z Docker Compose

### Instalacja i Uruchomienie

1. **Sklonuj repozytorium:**
   ```bash
   git clone [https://github.com/r-zab/smart-booking-system.git](https://github.com/r-zab/smart-booking-system.git)
   cd smart-booking-system
   ```

2. **Uruchom kontenery:**
   ```bash
   docker-compose up --build
   ```
   Komenda zbuduje obrazy, pobierze zależności i uruchomi kontenery dla aplikacji oraz bazy danych. Aplikacja będzie
   dostępna pod adresem `http://127.0.0.1:8000`.

3. **Przygotuj bazę danych (w drugim, osobnym oknie terminala):**
   ```bash
   # Zastosuj migracje, aby stworzyć tabele w bazie danych
   docker-compose exec app python manage.py migrate

   # Stwórz konto superużytkownika, aby móc zalogować się do panelu admina
   docker-compose exec app python manage.py createsuperuser

   # (Opcjonalnie) Wypełnij bazę danych predefiniowaną listą 20 zasobów
   docker-compose exec app python manage.py seed_resources
   
   # (Opcjonalnie) Wypełnij bazę danych 2500 losowymi rezerwacjami historycznymi
   docker-compose exec app python manage.py seed_data
   ```

4. **Gotowe!** Możesz teraz wejść na:
    * `http://127.0.0.1:8000/admin/` - aby zalogować się do panelu admina.
    * `http://127.0.0.1:8000/api/` - aby eksplorować API za pomocą interfejsu DRF.

### Uruchamianie Testów

Aby uruchomić zestaw testów automatycznych, użyj komendy:

```bash
    docker-compose exec app pytest
```

---

## Przykłady Użycia API

Poniżej kilka przykładów interakcji z API przy użyciu `curl`.  
Do uwierzytelnienia należy najpierw uzyskać token z endpointu `/api-token-auth/`.


### 1. Pobranie listy wszystkich zasobów
```bash
    curl -H "Authorization: Token twój_token_api" http://127.0.0.1:8000/api/resources/
```
### 2. Stworzenie nowej rezerwacji
```bash
    curl -X POST http://127.0.0.1:8000/api/bookings/ \
    -H "Authorization: Token twój_token_api" \
    -H "Content-Type: application/json" \
    -d '{
        "resource_id": 1,
        "start_time": "2025-08-10T14:00:00Z",
        "end_time": "2025-08-10T15:00:00Z",
        "title": "Spotkanie z klientem"
    }'
```
### 3. Zapytanie do chatbota
```bash
    curl -X POST http://127.0.0.1:8000/api/chatbot/ \
    -H "Authorization: Token twój_token_api" \
    -H "Content-Type: application/json" \
    -d '{
        "message": "sprawdź dostępność dla sala jupiter pojutrze o 12"
    }'
```
---

## Autor

* **Rafał Zaborek** - [r-zab](https://github.com/r-zab)