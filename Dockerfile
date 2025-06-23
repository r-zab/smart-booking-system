# Krok 1: Wybierz obraz bazowy
# Używamy oficjalnego, lekkiego obrazu z zainstalowanym Pythonem
FROM python:3.13-slim

# Krok 2: Ustaw zmienne środowiskowe
# Zapobiegają one buforowaniu logów i tworzeniu plików .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Krok 3: Ustaw katalog roboczy wewnątrz kontenera
WORKDIR /app

# Krok 4: Zainstaluj zależności
# Kopiujemy tylko plik z listą pakietów, aby wykorzystać cache'owanie Dockera
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Krok 5: Skopiuj cały kod aplikacji
# Kropka oznacza "wszystko z bieżącego folderu"
COPY . .