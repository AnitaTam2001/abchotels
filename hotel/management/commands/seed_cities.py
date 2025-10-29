# hotel/management/commands/seed_cities.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps

class Command(BaseCommand):
    help = 'Seed the database with sample cities and rooms'

    def handle(self, *args, **options):
        # Check if City model exists in database
        try:
            from hotel.models import City, RoomType, Room
            
            # Clear existing data only if tables exist
            try:
                City.objects.all().delete()
                Room.objects.all().delete()
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Could not clear existing data: {e}')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Models not available: {e}')
            )
            self.stdout.write(
                self.style.WARNING('Please run migrations first:')
            )
            self.stdout.write('python manage.py makemigrations hotel')
            self.stdout.write('python manage.py migrate')
            return

        # Now import after checking
        from hotel.models import City, RoomType, Room

        # Create cities
        cities_data = [
            {
                'name': 'New York',
                'description': 'Experience luxury in the heart of Manhattan. Our New York location offers stunning city views and premium amenities steps away from Central Park and Broadway.',
            },
            {
                'name': 'Los Angeles',
                'description': 'Stay in style in the City of Angels. Our LA hotel combines Hollywood glamour with modern comfort, located near Beverly Hills and downtown attractions.',
            },
            {
                'name': 'Chicago',
                'description': 'Discover Chicago from our premium downtown location. Enjoy breathtaking lake views and easy access to Magnificent Mile and Millennium Park.',
            },
            {
                'name': 'Miami',
                'description': 'Beachfront luxury in vibrant Miami. Our oceanfront property offers direct beach access, tropical pools, and South Beach nightlife.',
            },
            {
                'name': 'Las Vegas',
                'description': 'The ultimate Vegas experience on the Strip. Enjoy world-class entertainment, fine dining, and luxurious accommodations in the entertainment capital.',
            },
            {
                'name': 'San Francisco',
                'description': 'Iconic views in the Bay Area. Our San Francisco hotel offers stunning bay views, proximity to Fisherman\'s Wharf, and luxury in every detail.',
            },
        ]

        cities = {}
        for city_data in cities_data:
            city = City.objects.create(**city_data)
            cities[city_data['name']] = city
            self.stdout.write(
                self.style.SUCCESS(f'Created city: {city.name}')
            )

        # Create room types (if not exists)
        room_types_data = [
            {
                'name': 'Standard Room',
                'description': 'Comfortable room with queen bed, perfect for solo travelers or couples. Features a work desk, free WiFi, and modern amenities.',
                'price_per_night': 129.00,
                'capacity': 2
            },
            {
                'name': 'Deluxe Room',
                'description': 'Spacious room with king bed and sitting area. Enjoy premium amenities, city views, and enhanced comfort for your stay.',
                'price_per_night': 189.00,
                'capacity': 2
            },
            {
                'name': 'Executive Suite',
                'description': 'Luxurious suite with separate living area, king bed, and premium amenities. Perfect for business travelers or special occasions.',
                'price_per_night': 299.00,
                'capacity': 3
            },
            {
                'name': 'Presidential Suite',
                'description': 'Our most luxurious offering with multiple rooms, premium furnishings, and exclusive services. The ultimate hotel experience.',
                'price_per_night': 599.00,
                'capacity': 4
            }
        ]

        room_types = {}
        for room_type_data in room_types_data:
            room_type, created = RoomType.objects.get_or_create(
                name=room_type_data['name'],
                defaults=room_type_data
            )
            room_types[room_type_data['name']] = room_type
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created room type: {room_type.name}')
                )

        # Create rooms for each city
        for city_name, city in cities.items():
            for room_type_name, room_type in room_types.items():
                # Create 3-5 rooms of each type in each city
                room_count = 4 if room_type_name == 'Standard Room' else 3
                
                for i in range(1, room_count + 1):
                    Room.objects.create(
                        room_number=f"{city_name[:3].upper()}{room_type_name[:3].upper()}{i}",
                        room_type=room_type,
                        city=city,
                        is_available=True
                    )
            
            self.stdout.write(
                self.style.SUCCESS(f'Created rooms for {city.name}')
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with cities and rooms!')
        )