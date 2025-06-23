# booking/views.py

# --- Imports z bibliotek standardowych ---
import re
from datetime import date

# --- Imports z bibliotek firm trzecich ---
from dateparser.search import search_dates
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# --- Imports z naszej aplikacji ---
from .analysis import prepare_booking_data, train_prediction_model, get_future_predictions
from .models import Resource, Booking
from .serializers import ResourceSerializer, BookingSerializer

class ResourceViewSet(viewsets.ModelViewSet):  # <--- JEDYNA ZMIANA JEST TUTAJ
    """
    A ViewSet for viewing Resources.
    It automatically provides `list` and `retrieve` actions.
    """
    queryset = Resource.objects.all().order_by('id')
    serializer_class = ResourceSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        A custom action to get the 5 latest resources.
        """
        latest_resources = Resource.objects.order_by('-id')[:5]
        serializer = self.get_serializer(latest_resources, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Bookings.
    """
    queryset = Booking.objects.all().order_by('start_time')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    # === DODAJ TĘ METODĘ PONIŻEJ ===
    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user to the booking.
        """
        serializer.save(user=self.request.user)


# === DODAJ TEN NOWY WIDOK NA DOLE ===
class BookingDemandPredictionAPIView(APIView):
    """
    Zwraca prognozę zapotrzebowania na rezerwacje na następne 7 dni.
    """
    permission_classes = [IsAuthenticated]  # Od razu zabezpieczamy endpoint

    def get(self, request, *args, **kwargs):
        # Krok 1: Przygotuj dane z bazy
        booking_data = prepare_booking_data()

        if booking_data.empty or len(booking_data) < 2:
            # Zwracamy błąd, jeśli nie ma danych do analizy
            return Response({"error": "Brak wystarczających danych do stworzenia prognozy."}, status=400)

        # Krok 2: Wytrenuj model
        model = train_prediction_model(booking_data)

        if model is None:
            # Zwracamy błąd, jeśli trenowanie się nie powiodło
            return Response({"error": "Nie udało się wytrenować modelu predykcyjnego."}, status=500)

        # Krok 3: Wygeneruj prognozę na następne 7 dni
        predictions = get_future_predictions(model, days_to_predict=7)

        # Zwróć prognozę jako odpowiedź JSON
        return Response(predictions)


# ... istniejące importy i klasy ...

# === DODAJ TEN NOWY WIDOK NA DOLE ===
class ChatbotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # nlp = spacy.load... <- możemy usunąć lub zostawić, nie będziemy go już tu używać

    # === ZASTĄP STARĄ METODĘ POST TĄ PONIŻEJ ===
    def post(self, request, *args, **kwargs):
        user_message_original = request.data.get('message', '')
        if not user_message_original:
            return Response({'error': 'Wiadomość nie może być pusta.'}, status=400)

        # Normalizacja tekstu i wyszukiwanie słów kluczowych (bez zmian)
        def normalize_text(text):
            return re.sub(r"[^\w\s]", '', text.lower())

        user_keywords = set(normalize_text(user_message_original).split())

        best_match = None
        highest_score = 0
        for resource in Resource.objects.all():
            resource_keywords = set(normalize_text(resource.name).split())
            score = len(user_keywords.intersection(resource_keywords))
            if score > highest_score:
                highest_score = score
                best_match = resource

        found_resource = best_match

        # Rozpoznawanie daty (bez zmian)
        parsed_date_list = search_dates(user_message_original, languages=['pl'],
                                        settings={'PREFER_DATES_FROM': 'future'})
        found_date_str = None
        if parsed_date_list:
            found_date_str = parsed_date_list[0][1].strftime('%Y-%m-%d')

        # --- NOWA LOGIKA: SPRAWDZANIE BAZY DANYCH I ODPOWIADANIE ---

        bot_response_text = ""

        if found_resource and found_date_str:
            # Udało się zidentyfikować zasób ORAZ datę
            check_date = date.fromisoformat(found_date_str)

            # Szukamy rezerwacji dla danego zasobu w danym dniu
            bookings_on_day = Booking.objects.filter(
                resource=found_resource,
                start_time__date=check_date
            ).order_by('start_time')

            if not bookings_on_day.exists():
                bot_response_text = f"Wygląda na to, że zasób '{found_resource.name}' jest całkowicie wolny w dniu {found_date_str}."
            else:
                response_lines = [f"W dniu {found_date_str} zasób '{found_resource.name}' ma następujące rezerwacje:"]
                for booking in bookings_on_day:
                    start = booking.start_time.strftime('%H:%M')
                    end = booking.end_time.strftime('%H:%M')
                    response_lines.append(f"- od {start} do {end} ('{booking.title}')")
                bot_response_text = "\n".join(response_lines)

        elif found_resource:
            # Udało się zidentyfikować tylko zasób
            bot_response_text = f"Zrozumiałem, że pytasz o zasób '{found_resource.name}', ale nie podałeś daty. Spróbuj doprecyzować, np. 'jutro' lub '25 czerwca'."
        else:
            # Nie udało się zidentyfikować niczego
            bot_response_text = "Niestety, nie zrozumiałem o jaki zasób pytasz. Spróbuj podać bardziej konkretną nazwę."

        # --- Przygotowanie finalnej odpowiedzi ---
        response_data = {
            "original_message": user_message_original,
            "understood_entities": {
                "resource_name": found_resource.name if found_resource else None,
                "resource_id": found_resource.id if found_resource else None,
                "date": found_date_str
            },
            "bot_response": bot_response_text  # <--- Nasza nowa, wygenerowana odpowiedź
        }

        return Response(response_data)