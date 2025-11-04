# hotel/management/commands/import_room_types.py
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from hotel.models import RoomType

class Command(BaseCommand):
    help = 'Import room types with images from static/images/rooms directory'

    def handle(self, *args, **options):
        with transaction.atomic():
            self._process_room_types()

    def _process_room_types(self):
        # Room type data
        room_types_data = [
            {
                'name': 'Standard King',
                'description': 'Our comfortable Standard King room features a plush king-size bed, work desk, and modern amenities. Perfect for business travelers and couples.',
                'price_per_night': 159.00,
                'capacity': 2,
                'image': 'standard_king.png'
            },
            {
                'name': 'Standard Twin',
                'description': 'Ideal for friends or colleagues traveling together, our Standard Twin room offers two comfortable single beds and ample workspace.',
                'price_per_night': 149.00,
                'capacity': 2,
                'image': 'standard_twin.png'
            },
            {
                'name': 'Deluxe King',
                'description': 'Experience enhanced comfort in our Deluxe King room with premium bedding, sitting area, and upgraded amenities for a more luxurious stay.',
                'price_per_night': 199.00,
                'capacity': 2,
                'image': 'deluxe_king.png'
            },
            {
                'name': 'Deluxe Suite',
                'description': 'Our spacious Deluxe Suite features a separate living area, king bedroom, and premium amenities. Perfect for extended stays or special occasions.',
                'price_per_night': 299.00,
                'capacity': 3,
                'image': 'deluxe_suite.png'
            },
            {
                'name': 'Executive King',
                'description': 'Designed for the business traveler, our Executive King room offers enhanced workspace, premium amenities, and exclusive access to executive lounge.',
                'price_per_night': 249.00,
                'capacity': 2,
                'image': 'executive_king.png'
            },
            {
                'name': 'Executive Suite',
                'description': 'The ultimate business accommodation featuring separate living and working areas, premium technology, and exclusive executive benefits.',
                'price_per_night': 399.00,
                'capacity': 3,
                'image': 'executive_suite.png'
            },
            {
                'name': 'Presidential Suite',
                'description': 'Our most luxurious accommodation featuring multiple rooms, premium furnishings, panoramic views, and personalized butler service.',
                'price_per_night': 699.00,
                'capacity': 4,
                'image': 'presidential_suite.png'
            },
            {
                'name': 'Family Suite',
                'description': 'Perfect for families, this suite features separate bedrooms for parents and children, entertainment area, and family-friendly amenities.',
                'price_per_night': 349.00,
                'capacity': 4,
                'image': 'family_suite.png'
            },
            {
                'name': 'Honeymoon Suite',
                'description': 'Celebrate romance in our specially designed Honeymoon Suite featuring luxurious amenities, champagne service, and romantic decor.',
                'price_per_night': 449.00,
                'capacity': 2,
                'image': 'honeymoon_suite.png'
            },
        ]

        # Ensure media room_types directory exists
        media_rooms_dir = os.path.join(settings.MEDIA_ROOT, 'room_types')
        os.makedirs(media_rooms_dir, exist_ok=True)

        static_rooms_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'rooms')
        
        self.stdout.write(f"Looking for room images in: {static_rooms_dir}")
        
        if not os.path.exists(static_rooms_dir):
            self.stdout.write(self.style.ERROR(f'Static rooms directory not found: {static_rooms_dir}'))
            return

        available_images = os.listdir(static_rooms_dir)
        self.stdout.write(f"Available room images: {available_images}")

        success_count = 0
        error_count = 0

        for room_data in room_types_data:
            try:
                room_type, created = RoomType.objects.update_or_create(
                    name=room_data['name'],
                    defaults={
                        'description': room_data['description'],
                        'price_per_night': room_data['price_per_night'],
                        'capacity': room_data['capacity'],
                    }
                )

                image_filename = room_data['image']
                source_path = os.path.join(static_rooms_dir, image_filename)
                dest_path = os.path.join(media_rooms_dir, image_filename)
                
                if os.path.exists(source_path):
                    # Copy image to media directory
                    shutil.copy2(source_path, dest_path)
                    
                    # Assign image to room type
                    room_type.image.name = f'room_types/{image_filename}'
                    room_type.save()
                    
                    action = "Created" if created else "Updated"
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {action} {room_data["name"]}: {image_filename}')
                    )
                    success_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'✗ Image not found for {room_data["name"]}: {image_filename}')
                    )
                    error_count += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error with {room_data["name"]}: {str(e)}')
                )
                error_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Finished: {success_count} successful, {error_count} errors')
        )