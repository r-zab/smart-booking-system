from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from booking.views import UserCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('booking.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/register/', UserCreateAPIView.as_view(), name='register'),
]
