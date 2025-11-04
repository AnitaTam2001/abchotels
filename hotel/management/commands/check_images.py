# hotel/management/commands/check_images.py
import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Check available room images'

    def handle(self, *args, **options):
        # Check static images directory
        static_rooms_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'rooms')
        
        self.stdout.write("=== CHECKING STATIC IMAGES ===")
        self.stdout.write(f"Directory: {static_rooms_dir}")
        self.stdout.write(f"Exists: {os.path.exists(static_rooms_dir)}")
        
        if os.path.exists(static_rooms_dir):
            files = os.listdir(static_rooms_dir)
            self.stdout.write(f"Number of files: {len(files)}")
            for file in sorted(files):
                file_path = os.path.join(static_rooms_dir, file)
                file_size = os.path.getsize(file_path)
                self.stdout.write(f"  📁 {file} ({file_size} bytes)")
        else:
            self.stdout.write("❌ Static images directory not found!")
            
        # Check media images directory
        media_rooms_dir = os.path.join(settings.MEDIA_ROOT, 'room_types')
        
        self.stdout.write("\n=== CHECKING MEDIA IMAGES ===")
        self.stdout.write(f"Directory: {media_rooms_dir}")
        self.stdout.write(f"Exists: {os.path.exists(media_rooms_dir)}")
        
        if os.path.exists(media_rooms_dir):
            files = os.listdir(media_rooms_dir)
            self.stdout.write(f"Number of files: {len(files)}")
            for file in sorted(files):
                file_path = os.path.join(media_rooms_dir, file)
                file_size = os.path.getsize(file_path)
                self.stdout.write(f"  📁 {file} ({file_size} bytes)")
        else:
            self.stdout.write("ℹ️  Media images directory not found (this is normal if no imports have run)")