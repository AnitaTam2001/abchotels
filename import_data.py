# import_data.py
import os
import sys
import django
import csv

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abchotels.settings')
django.setup()

from hotel.models import City, RoomType, Room, Department, JobListing

def import_csv_data():
    base_path = os.path.join(os.path.dirname(__file__), 'csv')
    
    # Import Cities
    with open(os.path.join(base_path, 'cities.csv'), 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            City.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'description': row['description'],
                    'is_active': bool(int(row['is_active']))
                }
            )
    print("Cities imported successfully!")
    
    # Import Room Types
    with open(os.path.join(base_path, 'room_types.csv'), 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            RoomType.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'description': row['description'],
                    'price_per_night': float(row['price_per_night']),
                    'capacity': int(row['capacity'])
                }
            )
    print("Room types imported successfully!")
    
    # Import Rooms
    with open(os.path.join(base_path, 'rooms.csv'), 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Room.objects.get_or_create(
                id=row['id'],
                defaults={
                    'room_number': row['room_number'],
                    'room_type_id': row['room_type_id'],
                    'city_id': row['city_id'],
                    'is_available': bool(int(row['is_available']))
                }
            )
    print("Rooms imported successfully!")
    
    # Import Departments
    with open(os.path.join(base_path, 'departments.csv'), 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Department.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'description': row['description']
                }
            )
    print("Departments imported successfully!")
    
    # Import Jobs
    with open(os.path.join(base_path, 'jobs.csv'), 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            JobListing.objects.get_or_create(
                id=row['id'],
                defaults={
                    'title': row['title'],
                    'department_id': row['department_id'],
                    'job_type': row['job_type'],
                    'experience_level': row['experience_level'],
                    'location': row['location'],
                    'salary_range': row['salary_range'],
                    'description': row['description'],
                    'requirements': row['requirements'],
                    'responsibilities': row['responsibilities'],
                    'benefits': row['benefits'],
                    'is_active': bool(int(row['is_active'])),
                    'application_deadline': row['application_deadline'] if row['application_deadline'] else None
                }
            )
    print("Jobs imported successfully!")

if __name__ == '__main__':
    import_csv_data()