from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Dodajemy nasz nowy widok analityczny do importów
from .views import ResourceViewSet, BookingViewSet, BookingDemandPredictionAPIView, ChatbotAPIView

router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'bookings', BookingViewSet, basename='booking')

app_name = 'booking'

# Musimy zmodyfikować urlpatterns, aby zawierały zarówno adresy z routera,
# jak i nasz niestandardowy adres.
urlpatterns = [
    path('', include(router.urls)),
    path('analytics/demand_prediction/', BookingDemandPredictionAPIView.as_view(), name='demand-prediction'),
    # === DODAJ TĘ NOWĄ LINIJKĘ ===
    path('chatbot/', ChatbotAPIView.as_view(), name='chatbot'),
]