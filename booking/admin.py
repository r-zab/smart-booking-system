from django.contrib import admin
from .models import Resource, Booking

# Rejestracja modeli, aby były widoczne w panelu admina
admin.site.register(Resource)
admin.site.register(Booking)