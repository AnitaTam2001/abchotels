# hotel/management/commands/debug_room_types.py
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from hotel.models import RoomType

class Command(BaseCommand):
    help = 'Debug room types and images'

    def handle(self, *args, **options):
        # Check static directory
        static_rooms_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'rooms')
        self.stdout.write(f"Static rooms directory: {static_rooms_dir}")
        self.stdout.write(f"Directory exists: {os.path.exists(static_rooms_dir)}")
        
        if os.path.exists(static_rooms_dir):
            files = os.listdir(static_rooms_dir)
            self.stdout.write(f"Files in static/rooms: {files}")
        else:
            self.stdout.write("❌ Static rooms directory does not exist!")
            return

        # Check media directory
        media_rooms_dir = os.path.join(settings.MEDIA_ROOT, 'room_types')
        self.stdout.write(f"Media rooms directory: {media_rooms_dir}")
        self.stdout.write(f"Directory exists: {os.path.exists(media_rooms_dir)}")
        
        if os.path.exists(media_rooms_dir):
            files = os.listdir(media_rooms_dir)
            self.stdout.write(f"Files in media/room_types: {files}")

        # Check RoomType objects in database
        self.stdout.write("\n--- RoomType Objects in Database ---")
        room_types = RoomType.objects.all()
        
        if not room_types:
            self.stdout.write("❌ No RoomType objects found in database!")
            return

        for rt in room_types:
            self.stdout.write(f"\nRoomType: {rt.name}")
            self.stdout.write(f"  - Has image: {bool(rt.image)}")
            self.stdout.write(f"  - Image name: {rt.image.name if rt.image else 'None'}")
            self.stdout.write(f"  - Image URL: {rt.image.url if rt.image else 'None'}")
            
            if rt.image:
                # Check if file actually exists
                image_path = os.path.join(settings.MEDIA_ROOT, rt.image.name)
                self.stdout.write(f"  - File exists: {os.path.exists(image_path)}")
                self.stdout.write(f"  - Full path: {image_path}")