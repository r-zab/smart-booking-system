from django.contrib import admin
from django.urls import path, include  # WAŻNE: Dodajemy tutaj 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('booking.urls')), # To jest nasza nowa, kluczowa linijka
]