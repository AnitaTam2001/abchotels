# hotel/management/commands/simple_import_room_types.py
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from hotel.models import RoomType

class Command(BaseCommand):
    help = 'Simple room type import with better error handling'

    def handle(self, *args, **options):
        # Ensure directories exist
        media_rooms_dir = os.path.join(settings.MEDIA_ROOT, 'room_types')
        os.makedirs(media_rooms_dir, exist_ok=True)
        
        static_rooms_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'rooms')
        
        if not os.path.exists(static_rooms_dir):
            self.stdout.write(self.style.ERROR(f"❌ Static directory not found: {static_rooms_dir}"))
            return

        # Room types data
        room_data = [
            {'name': 'Standard King', 'price': 159, 'capacity': 2, 'image': 'standard_king.png', 
             'desc': 'Comfortable king room with modern amenities'},
            {'name': 'Standard Twin', 'price': 149, 'capacity': 2, 'image': 'standard_twin.png',
             'desc': 'Two single beds, perfect for friends traveling together'},
            {'name': 'Deluxe King', 'price': 199, 'capacity': 2, 'image': 'deluxe_king.png',
             'desc': 'Enhanced comfort with premium bedding and sitting area'},
            {'name': 'Deluxe Suite', 'price': 299, 'capacity': 3, 'image': 'deluxe_suite.png',
             'desc': 'Spacious suite with separate living area'},
            {'name': 'Executive King', 'price': 249, 'capacity': 2, 'image': 'executive_king.png',
             'desc': 'Business-focused with enhanced workspace'},
            {'name': 'Executive Suite', 'price': 399, 'capacity': 3, 'image': 'executive_suite.png',
             'desc': 'Ultimate business accommodation'},
            {'name': 'Presidential Suite', 'price': 699, 'capacity': 4, 'image': 'presidential_suite.png',
             'desc': 'Most luxurious accommodation'},
            {'name': 'Family Suite', 'price': 349, 'capacity': 4, 'image': 'family_suite.png',
             'desc': 'Perfect for families with separate bedrooms'},
            {'name': 'Honeymoon Suite', 'price': 449, 'capacity': 2, 'image': 'honeymoon_suite.png',
             'desc': 'Romantic suite for special occasions'},
        ]

        for data in room_data:
            try:
                # Delete existing room type to start fresh
                RoomType.objects.filter(name=data['name']).delete()
                
                # Create new room type
                room_type = RoomType.objects.create(
                    name=data['name'],
                    description=data['desc'],
                    price_per_night=data['price'],
                    capacity=data['capacity']
                )

                image_path = os.path.join(static_rooms_dir, data['image'])
                
                if os.path.exists(image_path):
                    # Copy to media directory
                    media_image_path = os.path.join(media_rooms_dir, data['image'])
                    shutil.copy2(image_path, media_image_path)
                    
                    # Assign using the actual file
                    with open(media_image_path, 'rb') as f:
                        room_type.image.save(data['image'], File(f), save=True)
                    
                    self.stdout.write(self.style.SUCCESS(f"✅ {data['name']} - {data['image']}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️  Image not found: {data['image']}"))
                    # Create room type anyway without image
                    room_type.save()
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ {data['name']} - Error: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("🎉 Room type import completed!"))