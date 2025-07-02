from rest_framework import serializers
from .models import Resource, Booking # Dodajemy Booking do importu
from django.contrib.auth.models import User # <--- DODAJ TEN IMPORT
from django.utils import timezone

# === DODAJ TĘ NOWĄ KLASĘ ===
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
# Ten serializer już mamy
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'capacity']

# === DODAJ TEN NOWY SERIALIZER PONIŻEJ ===
class BookingSerializer(serializers.ModelSerializer):
    # --- Pola tylko do ODZYTU ---
    # Te pola będą widoczne w odpowiedzi JSON, pokazując pełne, zagnieżdżone dane.
    # Oznaczamy je jako `read_only=True`, więc nie będą używane w formularzach zapisu.
    user = UserSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)

    # --- Pole tylko do ZAPISU ---
    # To pole pojawi się w formularzu i będzie oczekiwać ID zasobu.
    # Nie będzie widoczne w odpowiedzi JSON, tylko przy tworzeniu/edycji.
    resource_id = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.all(), source='resource', write_only=True
    )

    class Meta:
        model = Booking
        # W polach `fields` wymieniamy wszystkie pola, których chcemy używać
        fields = [
            'id',
            'resource',         # pole do odczytu (pełny obiekt)
            'user',             # pole do odczytu (pełny obiekt)
            'resource_id',      # pole do zapisu (tylko ID)
            'start_time',
            'end_time',
            'title',
        ]

    def validate(self, data):
        """
        Sprawdza, czy rezerwacja nie koliduje z istniejącymi rezerwacjami
        dla danego zasobu i czy daty są poprawne.
        """
        start_time = data['start_time']
        end_time = data['end_time']
        resource = data.get('resource')  # Używamy .get(), bo 'resource' jest write_only

        # Sprawdzenie, czy data końcowa nie jest przed początkową
        if end_time <= start_time:
            raise serializers.ValidationError("Data końcowa musi być po dacie początkowej.")

        # Sprawdzenie nakładania się terminów (kluczowa logika)
        # Szukamy rezerwacji dla tego samego zasobu, które nakładają się na nasz nowy termin.
        # Dwa terminy (A i B) nakładają się, jeśli (startA < endB) i (endA > startB).
        conflicting_bookings = Booking.objects.filter(
            resource=resource,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if conflicting_bookings:
            raise serializers.ValidationError(
                f"Zasób '{resource.name}' jest już zarezerwowany w tym terminie."
            )

        return data  # Zawsze zwracaj zwalidowane dane

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email') # Możemy też dodać np. 'first_name', 'last_name'

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user