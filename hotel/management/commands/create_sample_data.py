# hotel/management/commands/create_sample_data.py - UPDATED VERSION
from django.core.management.base import BaseCommand
from hotel.models import City, RoomType, Room

class Command(BaseCommand):
    help = 'Create sample data for hotels'

    def handle(self, *args, **options):
        # Create Cities with images
        cities_data = [
            {
                'name': 'New York', 
                'description': 'Experience luxury in the heart of Manhattan.',
                'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'name': 'Los Angeles', 
                'description': 'Stylish accommodations in downtown LA.',
                'image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'name': 'Chicago', 
                'description': 'Modern hotel with stunning city views.',
                'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'name': 'Miami', 
                'description': 'Beachfront luxury in South Beach.',
                'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'name': 'Las Vegas', 
                'description': 'Premium accommodations on the Strip.',
                'image_url': 'https://images.unsplash.com/photo-1605236453806-6ff36851218e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'name': 'San Francisco', 
                'description': 'Iconic hotel with bay views.',
                'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'name': 'London', 
                'description': 'Classic elegance in central London.',
                'image_url': 'https://images.unsplash.com/photo-1522798514-97ceb8c4f1c8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'name': 'Paris', 
                'description': 'Romantic hotel near the Eiffel Tower.',
                'image_url': 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'name': 'Tokyo', 
                'description': 'Modern luxury in the heart of Tokyo.',
                'image_url': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            },
            {
                'name': 'Dubai', 
                'description': 'Ultimate luxury with breathtaking views.',
                'image_url': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
            }
        ]
        
        # ... rest of your room types and rooms creation code remains the same