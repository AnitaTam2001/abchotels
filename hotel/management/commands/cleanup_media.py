# hotel/management/commands/cleanup_media.py
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from hotel.models import RoomType

class Command(BaseCommand):
    help = 'Clean up duplicate media files'

    def handle(self, *args, **options):
        media_rooms_dir = os.path.join(settings.MEDIA_ROOT, 'room_types')
        
        # Get all files currently in use by RoomType objects
        used_files = set()
        for rt in RoomType.objects.all():
            if rt.image:
                used_files.add(os.path.basename(rt.image.name))
        
        self.stdout.write(f"Files currently in use: {used_files}")
        
        # List all files in media directory
        all_files = os.listdir(media_rooms_dir)
        self.stdout.write(f"Total files in media: {len(all_files)}")
        
        # Find unused files
        unused_files = [f for f in all_files if f not in used_files]
        self.stdout.write(f"Unused files: {len(unused_files)}")
        
        # Delete unused files (commented out for safety - uncomment to actually delete)
        for file in unused_files:
            file_path = os.path.join(media_rooms_dir, file)
            self.stdout.write(f"Would delete: {file}")
            # Uncomment the next line to actually delete files
            # os.remove(file_path)
        
        self.stdout.write(self.style.SUCCESS("Cleanup completed (files not actually deleted - uncomment os.remove to delete)"))