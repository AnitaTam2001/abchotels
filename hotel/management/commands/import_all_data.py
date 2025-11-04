# hotel/management/commands/import_all_data.py
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Import all data: cities and room types'

    def handle(self, *args, **options):
        self.stdout.write("Starting data import process...")
        
        # Import cities
        self.stdout.write("\n1. Importing cities...")
        call_command('import_cities')
        
        # Import room types
        self.stdout.write("\n2. Importing room types...")
        call_command('import_room_types')
        
        # Assign city images
        self.stdout.write("\n3. Assigning city images...")
        call_command('fix_city_images')
        
        self.stdout.write(
            self.style.SUCCESS("\n✅ All data imported successfully!")
        )