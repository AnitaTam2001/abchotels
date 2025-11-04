# hotel/management/commands/import_cities.py
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from hotel.models import City

class Command(BaseCommand):
    help = 'Import cities with descriptions'

    def handle(self, *args, **options):
        # City data with descriptions
        cities_data = [
            {
                'name': 'New York',
                'description': 'Experience the vibrant energy of New York City with our luxury hotels located in prime Manhattan locations. Perfect for business and leisure travelers alike.',
            },
            {
                'name': 'London',
                'description': 'Discover historic charm meets modern luxury in the heart of London. Our hotels offer easy access to iconic landmarks and cultural attractions.',
            },
            {
                'name': 'Paris',
                'description': 'Immerse yourself in the romance and elegance of Paris. Our hotels provide stunning views and authentic Parisian experiences.',
            },
            {
                'name': 'Tokyo',
                'description': 'Experience the perfect blend of traditional culture and cutting-edge technology in Tokyo. Our hotels offer unparalleled service and comfort.',
            },
            {
                'name': 'Singapore',
                'description': 'Enjoy world-class luxury in the garden city. Our Singapore hotels feature stunning architecture and exceptional amenities.',
            },
            {
                'name': 'Sydney',
                'description': 'Wake up to breathtaking harbor views in Sydney. Our properties offer premium accommodations with iconic Opera House vistas.',
            },
            {
                'name': 'Rome',
                'description': 'Step into history with our luxury hotels in the eternal city. Experience Roman elegance and timeless beauty.',
            },
            {
                'name': 'Barcelona',
                'description': 'Enjoy Mediterranean charm and Gaudí architecture in vibrant Barcelona. Our hotels capture the city\'s unique spirit.',
            },
            {
                'name': 'Los Angeles',
                'description': 'Live the California dream in Los Angeles. Our hotels offer star treatment in the entertainment capital of the world.',
            },
            {
                'name': 'Miami',
                'description': 'Experience tropical luxury and art deco glamour in Miami. Our beachfront properties redefine coastal living.',
            },
            {
                'name': 'Las Vegas',
                'description': 'Indulge in ultimate luxury on the Las Vegas Strip. Our hotels offer world-class entertainment and premium accommodations.',
            },
            {
                'name': 'Chicago',
                'description': 'Discover architectural marvels and deep-dish charm in Chicago. Our hotels offer stunning skyline views and urban sophistication.',
            },
            {
                'name': 'San Francisco',
                'description': 'Experience the iconic hills and bay views of San Francisco. Our hotels combine tech innovation with classic California style.',
            },
            {
                'name': 'Amsterdam',
                'description': 'Explore charming canals and historic architecture in Amsterdam. Our hotels offer authentic Dutch hospitality.',
            },
            {
                'name': 'Vienna',
                'description': 'Immerse yourself in classical music and imperial history in Vienna. Our hotels embody Austrian elegance and culture.',
            },
            {
                'name': 'Prague',
                'description': 'Discover the fairy-tale beauty of Prague. Our hotels in the historic city center offer magical experiences.',
            },
        ]

        cities_created = 0
        cities_updated = 0

        for city_data in cities_data:
            city, created = City.objects.update_or_create(
                name=city_data['name'],
                defaults={
                    'description': city_data['description'],
                    'is_active': True
                }
            )
            
            if created:
                cities_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created city: {city.name}')
                )
            else:
                cities_updated += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated city: {city.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {cities_created + cities_updated} cities '
                f'({cities_created} created, {cities_updated} updated)'
            )
        )