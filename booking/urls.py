from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Dodajemy BookingViewSet do importu
from .views import ResourceViewSet, BookingViewSet

# Tworzymy router
router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resource')
# === DODAJ TĘ NOWĄ LINIJKĘ PONIŻEJ ===
router.register(r'bookings', BookingViewSet, basename='booking')

app_name = 'booking'

# Adresy URL naszej aplikacji są teraz automatycznie generowane przez router.
urlpatterns = router.urls