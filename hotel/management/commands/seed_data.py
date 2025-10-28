# hotel/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from hotel.models import RoomType, Room

class Command(BaseCommand):
    help = 'Seed the database with sample room data'

    def handle(self, *args, **options):
        # Clear existing data
        RoomType.objects.all().delete()
        Room.objects.all().delete()

        # Create room types
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

        for room_type_data in room_types_data:
            room_type = RoomType.objects.create(**room_type_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created room type: {room_type.name}')
            )

            # Create rooms for each type
            if room_type.name == 'Standard Room':
                for i in range(1, 6):
                    Room.objects.create(
                        room_number=f'10{i}',
                        room_type=room_type,
                        is_available=True
                    )
            elif room_type.name == 'Deluxe Room':
                for i in range(1, 6):
                    Room.objects.create(
                        room_number=f'20{i}',
                        room_type=room_type,
                        is_available=True
                    )
            elif room_type.name == 'Executive Suite':
                for i in range(1, 4):
                    Room.objects.create(
                        room_number=f'30{i}',
                        room_type=room_type,
                        is_available=True
                    )
            elif room_type.name == 'Presidential Suite':
                for i in range(1, 3):
                    Room.objects.create(
                        room_number=f'40{i}',
                        room_type=room_type,
                        is_available=True
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data!')
        )