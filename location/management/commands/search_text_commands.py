from django.core.management.base import BaseCommand
from ...models import Airport, City, Country


class Command(BaseCommand):
    help = 'Tum location app alanlari icin search_text sutunu olusturur.'

    def handle(self, *args, **options):
        # airport modeli icin guncelleme
        airports = Airport.objects.all()
        for airport in airports:
            airport.search_text = f'{airport.name},{airport.city.name},{airport.country.name}'
            airport.save()

        # city modeli icin guncelleme
        cities = City.objects.all()
        for city in cities:
            city.search_text = f'{city.name},{city.country.name}'
            city.save()

        # country modeli icin guncelleme
        countries = Country.objects.all()
        for country in countries:
            country.search_text = country.name
            country.save()

        self.stdout.write(self.style.SUCCESS('Tum location app modelleri icin search_text sutunu duzenlendi.'))
