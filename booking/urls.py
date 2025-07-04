from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet, BookingViewSet, BookingDemandPredictionAPIView, ChatbotAPIView

router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'bookings', BookingViewSet, basename='booking')

app_name = 'booking'

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/demand_prediction/', BookingDemandPredictionAPIView.as_view(), name='demand-prediction'),
    path('chatbot/', ChatbotAPIView.as_view(), name='chatbot'),
]
