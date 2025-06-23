import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import IntegrityError, transaction
from booking.models import Resource, Booking
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seeds the database with a large number of historical bookings.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old bookings...')
        # Czyścimy stare rezerwacje, aby zacząć na czysto
        Booking.objects.all().delete()
        self.stdout.write('Old bookings deleted.')

        self.stdout.write('Seeding new data...')

        users = list(User.objects.all())
        resources = list(Resource.objects.all())

        if not users or not resources:
            self.stdout.write(
                self.style.ERROR('Brak użytkowników lub zasobów w bazie. Dodaj je najpierw w panelu admina.'))
            return

        # ZMIANA: Definiujemy przedział czasowy
        today = timezone.now()
        one_year_ago = today - timedelta(days=365)

        booking_count = 0

        # Używamy `transaction.atomic`, aby przyspieszyć proces tworzenia wielu obiektów
        with transaction.atomic():
            # ZMIANA: Tworzymy 2500 rezerwacji
            for _ in range(2500):
                try:
                    random_resource = random.choice(resources)
                    random_user = random.choice(users)

                    # ZMIANA: Logika losowania daty w ostatnim roku
                    time_difference_in_seconds = (today - one_year_ago).total_seconds()
                    random_seconds = random.uniform(0, time_difference_in_seconds)
                    start_time = one_year_ago + timedelta(seconds=random_seconds)

                    duration = timedelta(hours=random.randint(1, 4), minutes=random.choice([0, 30]))
                    end_time = start_time + duration

                    # Sprawdzamy naszą walidację w kodzie, aby unikać niepotrzebnych zapytań do bazy
                    conflicting = Booking.objects.filter(
                        resource=random_resource,
                        start_time__lt=end_time,
                        end_time__gt=start_time
                    ).exists()

                    if not conflicting:
                        Booking.objects.create(
                            resource=random_resource,
                            user=random_user,
                            start_time=start_time,
                            end_time=end_time,
                            title=f"Losowa rezerwacja dla {random_resource.name}"
                        )
                        booking_count += 1
                except Exception:
                    # Ignorujemy błędy, np. gdyby walidacja w modelu/serializerze jednak coś znalazła
                    pass

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {booking_count} new historical bookings.'))