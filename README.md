# Inteligentny System Rezerwacji Zasobów (AI-Powered Booking System)

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Django](https://img.shields.io/badge/django-5.2-green.svg)
![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

**Zaawansowany system backendowy do rezerwacji zasobów firmowych, wyposażony w REST API oraz moduły sztucznej inteligencji do predykcji i interakcji w języku naturalnym.**

---

## 🧐 O Projekcie

Celem tego projektu było stworzenie w pełni funkcjonalnego, solidnego i skalowalnego systemu backendowego, który odzwierciedla realne wyzwania biznesowe. Aplikacja nie jest prostym CRUD-em – implementuje zaawansowaną logikę walidacji, zabezpieczenia oparte na uwierzytelnianiu oraz dwa odrębne moduły AI, demonstrując umiejętności wykraczające poza podstawy web developmentu.

Projekt został w całości skonteneryzowany przy użyciu Dockera, co zapewnia spójność środowiska i łatwość wdrożenia.

### ✨ Kluczowe Funkcjonalności

* **REST API:**
    * Pełna obsługa CRUD dla zasobów i rezerwacji.
    * Zaawansowane, zagnieżdżone serializery dla czytelnych odpowiedzi JSON.
    * Niestandardowe endpointy dla logiki biznesowej (np. `/latest/`).
* **Logika Biznesowa i Bezpieczeństwo:**
    * Walidacja zapobiegająca tworzeniu rezerwacji w zajętych terminach.
    * Automatyczne przypisywanie rezerwacji do zalogowanego użytkownika.
    * Wszystkie kluczowe endpointy zabezpieczone – dostępne tylko dla uwierzytelnionych użytkowników.
* **Moduł Predykcyjny (AI):**
    * Endpoint `/api/analytics/demand_prediction/` analizuje dane historyczne.
    * Wykorzystuje prosty model regresji liniowej (`scikit-learn`) do prognozowania zapotrzebowania na rezerwacje w przyszłości.
* **Inteligentny Asystent (Chatbot AI):**
    * Endpoint `/api/chatbot/` do interakcji w języku naturalnym.
    * Wykorzystuje logikę dopasowywania słów kluczowych i wyspecjalizowaną bibliotekę `dateparser` do rozumienia zapytań użytkownika o dostępność zasobów w konkretnym dniu.

---

## 🛠️ Stos Technologiczny i Architektura

Projekt opiera się na nowoczesnych i sprawdzonych technologiach, tworząc solidną architekturę backendową.

* **Backend:** Python, Django, Django REST Framework
* **Baza Danych:** PostgreSQL (uruchomiona w kontenerze Docker)
* **AI / Analiza Danych:** Pandas, Scikit-learn, dateparser
* **Konteneryzacja:** Docker, Docker Compose
* **Testowanie:** Pytest, pytest-django

Architektura systemu składa się z dwóch głównych kontenerów zarządzanych przez `docker-compose`: serwisu `app` z aplikacją Django oraz serwisu `db` z bazą danych PostgreSQL, które komunikują się ze sobą w izolowanej sieci wirtualnej.

---

## 🚀 Jak Uruchomić Projekt

Dzięki konteneryzacji, uruchomienie projektu jest niezwykle proste.

### Wymagania Wstępne

* Zainstalowany [Git](https://git-scm.com/)
* Zainstalowany [Docker](https://www.docker.com/products/docker-desktop/) z Docker Compose

### Instalacja i Uruchomienie

1.  **Sklonuj repozytorium:**
    ```bash
    git clone [https://github.com/r-zab/smart-booking-system.git](https://github.com/r-zab/smart-booking-system.git)
    cd smart-booking-system
    ```

2.  **Uruchom kontenery:**
    ```bash
    docker-compose up --build
    ```
    Komenda zbuduje obrazy, pobierze zależności i uruchomi kontenery dla aplikacji oraz bazy danych. Aplikacja będzie dostępna pod adresem `http://127.0.0.1:8000`.

3.  **Przygotuj bazę danych (w drugim, osobnym oknie terminala):**
    ```bash
    # Zastosuj migracje, aby stworzyć tabele w bazie danych
    docker-compose exec app python manage.py migrate

    # Stwórz konto superużytkownika, aby móc zalogować się do panelu admina
    docker-compose exec app python manage.py createsuperuser

    # (Opcjonalnie) Wypełnij bazę danych predefiniowaną listą 20 zasobów
    docker-compose exec app python manage.py seed_resources

    # (Opcjonalnie) Wypełnij bazę danych 2500 losowymi rezerwacjami
    docker-compose exec app python manage.py seed_data
    ```

4.  **Gotowe!** Możesz teraz wejść na:
    * `http://127.0.0.1:8000/admin/` - aby zalogować się do panelu admina.
    * `http://127.0.0.1:8000/api/` - aby eksplorować API.

### Uruchamianie Testów

Aby uruchomić zestaw testów automatycznych, użyj komendy:
```bash
docker-compose exec app pytest
```

---

## 🕹️ Przykłady Użycia API

Poniżej kilka przykładów interakcji z API przy użyciu `curl`. Wymagane jest uwierzytelnienie (tutaj `admin:twoje_haslo`).

**1. Pobranie listy wszystkich zasobów:**
```bash
curl -u admin:twoje_haslo [http://127.0.0.1:8000/api/resources/](http://127.0.0.1:8000/api/resources/)
```

**2. Stworzenie nowej rezerwacji:**
```bash
curl -u admin:twoje_haslo -X POST [http://127.0.0.1:8000/api/bookings/](http://127.0.0.1:8000/api/bookings/) \
-H "Content-Type: application/json" \
-d '{
    "resource_id": 1,
    "start_time": "2025-07-10T14:00:00Z",
    "end_time": "2025-07-10T15:00:00Z",
    "title": "Spotkanie z klientem"
}'
```

**3. Zapytanie do chatbota:**
```bash
curl -u admin:twoje_haslo -X POST [http://127.0.0.1:8000/api/chatbot/](http://127.0.0.1:8000/api/chatbot/) \
-H "Content-Type: application/json" \
-d '{
    "message": "sprawdź dostępność dla sala jupiter pojutrze"
}'
```

---

## 📈 Mapa Drogowa (Możliwe Ulepszenia)

* [ ] Rozbudowa modelu AI o dodatkowe cechy (dzień tygodnia, święta).
* [ ] Wprowadzenie ról i uprawnień na poziomie API (np. `guest` może tylko czytać).
* [ ] Stworzenie prostego frontendu w React lub Vue.js.
* [ ] Konfiguracja CI/CD na GitHub Actions do automatycznego uruchamiania testów.

---

## ✍️ Autor

* **Rafał Zaborek** - [r-zab](https://github.com/r-zab)