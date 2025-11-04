# hotel/management/commands/fix_city_images.py
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from hotel.models import City

class Command(BaseCommand):
    help = 'Copy city images to media directory and assign to cities'

    def handle(self, *args, **options):
        # Ensure media cities directory exists
        media_cities_dir = os.path.join(settings.MEDIA_ROOT, 'cities')
        os.makedirs(media_cities_dir, exist_ok=True)

        # Copy all images from static to media
        static_cities_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'cities')
        
        self.stdout.write(f"Looking for images in: {static_cities_dir}")
        
        if not os.path.exists(static_cities_dir):
            self.stdout.write(self.style.ERROR(f'Static cities directory not found: {static_cities_dir}'))
            self.stdout.write("Please make sure you have a 'static/images/cities' directory with city images.")
            return

        # List what images are available
        available_images = os.listdir(static_cities_dir)
        self.stdout.write(f"Available images: {available_images}")

        # Copy images and assign to cities
        city_image_map = {
            'New York': 'new_york.jpg',
            'London': 'london.jpg',
            'Paris': 'paris.jpg',
            'Tokyo': 'tokyo.jpg',
            'Singapore': 'singapore.jpg',
            'Sydney': 'sydney.jpg',
            'Rome': 'rome.jpg',
            'Barcelona': 'barcelona.jpg',
            'Los Angeles': 'los_angeles.jpg',
            'Miami': 'miami.jpg',
            'Las Vegas': 'las_vegas.jpg',
            'Chicago': 'chicago.jpg',
            'San Francisco': 'san_francisco.jpg',
            'Amsterdam': 'amsterdam.jpg',
            'Vienna': 'vienna.jpg',
            'Prague': 'prague.jpg',
        }

        success_count = 0
        error_count = 0

        for city_name, image_filename in city_image_map.items():
            try:
                source_path = os.path.join(static_cities_dir, image_filename)
                dest_path = os.path.join(media_cities_dir, image_filename)
                
                if os.path.exists(source_path):
                    # Copy image to media directory
                    shutil.copy2(source_path, dest_path)
                    
                    # Assign to city
                    city = City.objects.get(name=city_name)
                    city.image.name = f'cities/{image_filename}'
                    city.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {city_name}: {image_filename}')
                    )
                    success_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'✗ Image not found: {image_filename}')
                    )
                    error_count += 1
                    
            except City.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ City not found in database: {city_name}')
                )
                error_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error with {city_name}: {str(e)}')
                )
                error_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Finished: {success_count} successful, {error_count} errors')
        )