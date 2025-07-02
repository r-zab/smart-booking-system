# w pliku core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token # <--- NOWY IMPORT
from booking.views import UserCreateAPIView # <--- NOWY IMPORT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('booking.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/register/', UserCreateAPIView.as_view(), name='register'), # <--- NOWA LINIA
]