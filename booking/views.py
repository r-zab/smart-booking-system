import re
from datetime import date

from django.utils import timezone
from dateparser.search import search_dates
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from .serializers import ResourceSerializer, BookingSerializer, UserCreateSerializer
from django.contrib.auth.models import User

from .analysis import prepare_booking_data, train_prediction_model, get_future_predictions
from .models import Resource, Booking
from .serializers import ResourceSerializer, BookingSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all().order_by('id')
    serializer_class = ResourceSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_resources = Resource.objects.order_by('-id')[:5]
        serializer = self.get_serializer(latest_resources, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):

        resource = self.get_object()
        start_of_today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        bookings = resource.bookings.filter(
            end_time__gte=start_of_today
        ).order_by('start_time')

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('start_time')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user).order_by('-start_time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingDemandPredictionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        booking_data = prepare_booking_data()

        if booking_data.empty or len(booking_data) < 2:
            return Response({"error": "Brak wystarczających danych do stworzenia prognozy."}, status=400)

        model = train_prediction_model(booking_data)

        if model is None:
            return Response({"error": "Nie udało się wytrenować modelu predykcyjnego."}, status=500)

        predictions = get_future_predictions(model, days_to_predict=7)

        return Response(predictions)


class ChatbotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_message_original = request.data.get('message', '')
        if not user_message_original:
            return Response({'error': 'Wiadomość nie może być pusta.'}, status=400)

        def normalize_text(text):
            return re.sub(r"[^\w\s]", '', text.lower())

        user_message_normalized = normalize_text(user_message_original)
        user_keywords = set(user_message_normalized.split())

        best_match = None
        highest_score = 0
        for resource in Resource.objects.all():
            resource_keywords = set(normalize_text(resource.name).split())
            score = len(user_keywords.intersection(resource_keywords))
            if score > highest_score:
                highest_score = score
                best_match = resource

        found_resource = best_match

        parsed_date_list = search_dates(
            user_message_original,
            languages=['pl'],
            settings={'PREFER_DATES_FROM': 'future', 'RETURN_AS_TIMEZONE_AWARE': True}
        )

        found_datetime = parsed_date_list[0][1] if parsed_date_list else None

        bot_response_text = ""

        if found_resource and found_datetime:
            conflicting_booking = Booking.objects.filter(
                resource=found_resource,
                start_time__lt=found_datetime,
                end_time__gt=found_datetime
            ).first()

            if conflicting_booking:
                local_tz = timezone.get_current_timezone()
                local_start = conflicting_booking.start_time.astimezone(local_tz)
                local_end = conflicting_booking.end_time.astimezone(local_tz)

                bot_response_text = (
                    f"Niestety, o tej porze zasób '{found_resource.name}' jest już zajęty. "
                    f"Istnieje rezerwacja od {local_start.strftime('%H:%M')} do {local_end.strftime('%H:%M')}."
                )
            else:
                bot_response_text = f"Wygląda na to, że o tej porze zasób '{found_resource.name}' jest dostępny."

        elif found_resource:
            bot_response_text = f"Zrozumiałem, że pytasz o zasób '{found_resource.name}', ale nie podałeś daty i godziny. Spróbuj doprecyzować."
        else:
            bot_response_text = "Niestety, nie zrozumiałem o jaki zasób pytasz."

        response_data = {
            "original_message": user_message_original,
            "understood_entities": {
                "resource_name": found_resource.name if found_resource else None,
                "date_time": found_datetime.isoformat() if found_datetime else None,
            },
            "bot_response": bot_response_text
        }
        return Response(response_data)

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = []
