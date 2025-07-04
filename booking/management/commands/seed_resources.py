from django.core.management.base import BaseCommand
from booking.models import Resource

class Command(BaseCommand):
    help = 'Seeds the database with a predefined list of resources.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding resources...')

        RESOURCES = [
            {'name': "Sala Konferencyjna 'Jupiter'", 'description': 'Główna, reprezentacyjna sala na 1 piętrze.', 'capacity': 20},
            {'name': "Sala Spotkań 'Mars'", 'description': 'Standardowa sala spotkań z TV 65 cali i whiteboardem.', 'capacity': 8},
            {'name': "Pokój Kreatywny 'Wenus'", 'description': 'Nieformalna przestrzeń z pufami do burzy mózgów.', 'capacity': 10},
            {'name': "Pokój Cichej Pracy 'Merkury'", 'description': 'Wyciszony pokój jednoosobowy.', 'capacity': 1},
            {'name': "Sala Szkoleniowa 'Saturn'", 'description': 'Sala w układzie szkolnym z rzutnikiem.', 'capacity': 15},
            {'name': "Projektor Mobilny #1 (Epson)", 'description': 'Przenośny projektor Full HD w torbie z kablami.', 'capacity': 1},
            {'name': "Projektor Mobilny #2 (BenQ)", 'description': 'Zapasowy projektor przenośny.', 'capacity': 1},
            {'name': "Zestaw do Wideokonferencji (Logitech)", 'description': 'Przenośna kamera z mikrofonem dalekiego zasięgu.', 'capacity': 1},
            {'name': "Laptop dla Gościa #1 (Dell)", 'description': 'Laptop z podstawowym oprogramowaniem biurowym.', 'capacity': 1},
            {'name': "Samochód Służbowy #1 - Toyota Corolla", 'description': 'Samochód osobowy typu sedan.', 'capacity': 4},
            {'name': "Samochód Służbowy #2 - Skoda Octavia", 'description': 'Samochód osobowy typu kombi.', 'capacity': 5},
            {'name': "Rower Firmowy 'CityBike'", 'description': 'Rower miejski do dyspozycji pracowników.', 'capacity': 1},
            {'name': "Miejsce Parkingowe 'Gość #1'", 'description': 'Miejsce postojowe najbliżej wejścia.', 'capacity': 1},
            {'name': "Drukarka 3D (Prusa)", 'description': 'Drukarka 3D do prototypowania.', 'capacity': 1},
            {'name': "Licencja Pływająca - Adobe CC", 'description': 'Dostęp do pełnego pakietu Adobe Creative Cloud.', 'capacity': 1},
            {'name': "Aparat Fotograficzny (Sony A7 IV)", 'description': 'Profesjonalny aparat do użytku przez dział marketingu.', 'capacity': 1},
            {'name': "Dron Filmowy (DJI Mavic 3)", 'description': 'Zaawansowany dron do nagrywania materiałów wideo.', 'capacity': 1},
            {'name': "Hulajnoga elektryczna #1 (Xiaomi)", 'description': 'Składana hulajnoga elektryczna.', 'capacity': 1},
            {'name': "Strefa Relaksu 'Oaza'", 'description': 'Wydzielona strefa z konsolą do gier i kanapami.', 'capacity': 10},
            {'name': "Grill Gazowy (Taras)", 'description': 'Duży grill gazowy na tarasie firmowym.', 'capacity': 1},
        ]

        created_count = 0
        for resource_data in RESOURCES:
            resource, created = Resource.objects.get_or_create(
                name=resource_data['name'],
                defaults={
                    'description': resource_data['description'],
                    'capacity': resource_data['capacity']
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created resource: '{resource.name}'"))
                created_count += 1
            else:
                self.stdout.write(f"Resource '{resource.name}' already exists. Skipping.")

        self.stdout.write(self.style.SUCCESS(f'Seeding complete. Created {created_count} new resources.'))
