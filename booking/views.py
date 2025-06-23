from rest_framework import viewsets, response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated # <--- NOWY IMPORT
from .models import Resource, Booking
from .serializers import ResourceSerializer, BookingSerializer

class ResourceViewSet(viewsets.ModelViewSet): # <--- JEDYNA ZMIANA JEST TUTAJ
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
        return response.Response(serializer.data)

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