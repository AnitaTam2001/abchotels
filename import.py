# import.py - ABC Hotels Data Import System (With Duplicate Check)
import os
import sys
import django
import csv
import time

# Setup Django environment
sys.path.append('/Users/anita/abc')  # CHANGED: from abchotels to abc
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abchotels.settings')  # Keep this as is if your Django project name is still abchotels
django.setup()

from django.db import connection
from hotel.models import City, RoomType, Room, Department, Booking, FAQ, JobListing, JobApplication

CSV_FOLDER = 'csv'

def close_db_connection():
    """Explicitly close database connection to prevent locking"""
    try:
        connection.close()
        time.sleep(0.05)
    except Exception as e:
        print(f"X Could not close database connection: {e}")

def check_csv_files():
    """Check if all required CSV files exist"""
    print("Checking CSV files...")

    required_files = {
        'import_city.csv': 'Cities',
        'import_roomtype.csv': 'Room Types',
        'import_department.csv': 'Departments',
        'import_room.csv': 'Rooms'
    }

    missing_files = []

    for filename, description in required_files.items():
        filepath = os.path.join(CSV_FOLDER, filename)
        if os.path.exists(filepath):
            print(f"✓ {description}: {filename}")
        else:
            print(f"X {description}: {filename} - FILE NOT FOUND")
            missing_files.append(filename)

    if missing_files:
        print(f"\nX Missing {len(missing_files)} required CSV files:")
        for missing in missing_files:
            print(f" - {missing}")
        return False

    print(f"\n✓ All required CSV files found!")
    return True

def check_single_csv_file(filename, description):
    """Check if a single CSV file exists"""
    filepath = os.path.join(CSV_FOLDER, filename)
    if os.path.exists(filepath):
        print(f"✓ {description}: {filename}")
        return True
    else:
        print(f"X {description}: {filename} - FILE NOT FOUND")
        return False

def skip_comments_and_get_reader(file):
    """Skip comment lines and return CSV reader with proper header"""
    lines = []
    for line in file:
        if not line.strip().startswith('#'):
            lines.append(line)

    if lines:
        return csv.DictReader(lines)
    else:
        return None

def import_city(filename):
    """Import City data from CSV"""
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        print(f"Reading from: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                print("No data found in CSV file")
                return 0

            cities_created = 0
            cities_updated = 0

            for row in reader:
                # Use the image filename directly - assuming CSV has correct relative path
                image_filename = row['Image Filename']
                if image_filename:
                    # Use the filename as-is from CSV
                    image_path = image_filename
                else:
                    image_path = ''

                defaults = {
                    'name': row['Name'], 
                    'description': row['Description'], 
                    'is_active': row['Is Active'].lower() == 'true',
                    'image': image_path
                }

                city, created = City.objects.get_or_create(
                    id=row['ID'], 
                    defaults=defaults
                )

                if created:
                    cities_created += 1
                else:
                    # Update existing city
                    for key, value in defaults.items():
                        setattr(city, key, value)
                    city.save()
                    cities_updated += 1

                close_db_connection()

            print(f"Cities: {cities_created} created, {cities_updated} updated")
            return cities_created

    except Exception as e:
        print(f"Error importing cities: {e}")
        return 0

def import_roomtype(filename):
    """Import RoomType data from CSV"""
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        print(f"Reading from: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                print("No data found in CSV file")
                return 0
            
            roomtypes_created = 0
            roomtypes_updated = 0
            
            for row in reader:
                # Use the image filename directly - assuming CSV has correct relative path
                image_filename = row['Image Filename']
                if image_filename:
                    # Use the filename as-is from CSV
                    image_path = image_filename
                else:
                    image_path = ''

                defaults = {
                    'name': row['Name'], 
                    'description': row['Description'], 
                    'price_per_night': float(row['Price Per Night']),
                    'capacity': int(row['Capacity']),
                    'image': image_path
                }
                
                roomtype, created = RoomType.objects.get_or_create(
                    id=row['ID'], 
                    defaults=defaults
                )
                
                if created:
                    roomtypes_created += 1
                else:
                    # Update existing room type
                    for key, value in defaults.items():
                        setattr(roomtype, key, value)
                    roomtype.save()
                    roomtypes_updated += 1
                    
                close_db_connection()
                
            print(f"Room Types: {roomtypes_created} created, {roomtypes_updated} updated")
            return roomtypes_created
            
    except Exception as e:
        print(f"Error importing room types: {e}")
        return 0

def import_department(filename):
    """Import Department data from CSV"""
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        print(f"Reading from: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                print("No data found in CSV file")
                return 0

            departments_created = 0
            departments_updated = 0

            for row in reader:
                defaults = {
                    'name': row['Name'], 
                    'description': row['Description']
                }

                department, created = Department.objects.get_or_create(
                    id=row['ID'],
                    defaults=defaults
                )

                if created:
                    departments_created += 1
                else:
                    # Update existing department
                    for key, value in defaults.items():
                        setattr(department, key, value)
                    department.save()
                    departments_updated += 1

                close_db_connection()
                
            print(f"Departments: {departments_created} created, {departments_updated} updated")
            return departments_created

    except Exception as e:
        print(f"Error importing departments: {e}")
        return 0

def import_room(filename):
    """Import Room data from CSV with duplicate prevention"""
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        print(f"Reading from: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                print("No data found in CSV file")
                return 0

            rooms_created = 0
            rooms_skipped = 0
            missing_refs = 0

            for row in reader:
                try:
                    city = City.objects.get(id=row['City ID'])
                    room_type = RoomType.objects.get(id=row['Room Type ID'])

                    # Check if room with same ID already exists
                    if Room.objects.filter(id=row['ID']).exists():
                        print(f"^ Room {row['ID']} already exists - skipping")
                        rooms_skipped += 1
                        continue

                    room, created = Room.objects.get_or_create(
                        id=row['ID'],
                        defaults={
                            'city': city,
                            'room_type': room_type,
                            'is_available': row['Is Available'].lower() == 'true'
                        }
                    )

                    if created:
                        rooms_created += 1

                except City.DoesNotExist:
                    print(f"^ City ID {row['City ID']} not found for room {row['ID']}")
                    missing_refs += 1
                except RoomType.DoesNotExist:
                    print(f"^ RoomType ID {row['Room Type ID']} not found for room {row['ID']}")
                    missing_refs += 1
                    
                close_db_connection()
                
            print(f"✓ Rooms: {rooms_created} created")
            if rooms_skipped > 0:
                print(f"^ Skipped {rooms_skipped} duplicate rooms")
            if missing_refs > 0:
                print(f"^ Skipped {missing_refs} rooms due to missing references")
            return rooms_created

    except Exception as e:
        print(f"Error importing rooms: {e}")
        return 0

def import_all_data():
    """Import all data from CSV files"""
    print("# IMPORTING ALL HOTEL DATA FROM CSV FILES...")
    print("=" * 60)

    if not check_csv_files():
        print("\nX Cannot import data - missing CSV files!")
        return False

    total_records = 0

    import_steps = [
        ("Cities", "import_city.csv", import_city),
        ("Room Types", "import_roomtype.csv", import_roomtype),
        ("Departments", "import_department.csv", import_department),
        ("Rooms", "import_room.csv", import_room),
    ]

    print("\n" + "=" * 60)
    print("STARTING DATA IMPORT...")
    print("=" * 60)

    for step_name, filename, import_func in import_steps:
        print(f"\n→ Importing {step_name}...")
        records = import_func(filename)
        total_records += records
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("  IMPORT COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    print("\nFINAL DATABASE STATE:")
    print(f"    Cities: {City.objects.count()}")
    print(f"    Room Types: {RoomType.objects.count()}")
    print(f"    Rooms: {Room.objects.count()}")
    print(f"    Departments: {Department.objects.count()}")
    print(f"    Total Records: {total_records}")

    return True

def clean_all_data():
    """Clean all data from database"""
    print("  CLEANING ALL DATA...")
    print("=" * 50)

    models_to_clean = [
        ("Bookings", Booking),
        ("Job Applications", JobApplication),
        ("Job Listings", JobListing),
        ("FAQs", FAQ),
        ("Rooms", Room),
        ("Room Types", RoomType),
        ("Departments", Department),
        ("Cities", City),
    ]

    total_deleted = 0
    for model_name, model in models_to_clean:
        count = model.objects.count()
        model.objects.all().delete()
        close_db_connection()
        print(f" {model_name}: {count} deleted")
        total_deleted += count
        time.sleep(0.1)

    print("=" * 50)
    print(f" All data cleaned! {total_deleted} total records deleted")
    return True

def clean_cities():
    """Clean only cities data"""
    print("  CLEANING CITIES DATA...")
    print("=" * 40)
    
    count = City.objects.count()
    City.objects.all().delete()
    close_db_connection()
    print(f" Cities: {count} deleted")
    print("=" * 40)
    print(f" Cities data cleaned!")
    return True

def clean_room_types():
    """Clean only room types data"""
    print("  CLEANING ROOM TYPES DATA...")
    print("=" * 40)
    
    count = RoomType.objects.count()
    RoomType.objects.all().delete()
    close_db_connection()
    print(f" Room Types: {count} deleted")
    print("=" * 40)
    print(f" Room Types data cleaned!")
    return True

def clean_rooms():
    """Clean only rooms data"""
    print("  CLEANING ROOMS DATA...")
    print("=" * 40)
    
    count = Room.objects.count()
    Room.objects.all().delete()
    close_db_connection()
    print(f" Rooms: {count} deleted")
    print("=" * 40)
    print(f" Rooms data cleaned!")
    return True

def import_cities_only():
    """Import only cities data"""
    print("  IMPORTING CITIES...")
    print("=" * 40)
    
    if not check_single_csv_file('import_city.csv', 'Cities'):
        print("\nX Cannot import cities - CSV file not found!")
        return False
    
    records = import_city('import_city.csv')
    print("=" * 40)
    print(f" Cities import completed! {records} records imported")
    return True

def import_room_types_only():
    """Import only room types data"""
    print("  IMPORTING ROOM TYPES...")
    print("=" * 40)
    
    if not check_single_csv_file('import_roomtype.csv', 'Room Types'):
        print("\nX Cannot import room types - CSV file not found!")
        return False
    
    records = import_roomtype('import_roomtype.csv')
    print("=" * 40)
    print(f" Room Types import completed! {records} records imported")
    return True

def import_rooms_only():
    """Import only rooms data"""
    print("  IMPORTING ROOMS...")
    print("=" * 40)
    
    if not check_single_csv_file('import_room.csv', 'Rooms'):
        print("\nX Cannot import rooms - CSV file not found!")
        return False
    
    records = import_room('import_room.csv')
    print("=" * 40)
    print(f" Rooms import completed! {records} records imported")
    return True

def import_departments_only():
    """Import only departments data"""
    print("  IMPORTING DEPARTMENTS...")
    print("=" * 40)
    
    if not check_single_csv_file('import_department.csv', 'Departments'):
        print("\nX Cannot import departments - CSV file not found!")
        return False
    
    records = import_department('import_department.csv')
    print("=" * 40)
    print(f" Departments import completed! {records} records imported")
    return True

def show_current_state():
    """Show current database state"""
    print("\nCURRENT DATABASE STATE:")
    print(f"  Cities: {City.objects.count()}")
    print(f"  Room Types: {RoomType.objects.count()}")
    print(f"  Rooms: {Room.objects.count()}")
    print(f"  Departments: {Department.objects.count()}")

def main():
    """Main program loop"""
    if not os.path.exists(CSV_FOLDER):
        os.makedirs(CSV_FOLDER)

    while True:
        print("\n" + "=" * 50)
        print(" ABC HOTELS - DATA MANAGEMENT SYSTEM")
        print("=" * 50)

        show_current_state()

        print("=" * 50)
        print("1. CLEAN ALL DATA")
        print("2. CLEAN ALL CITIES")
        print("3. CLEAN ALL ROOM TYPES")
        print("4. CLEAN ALL ROOMS")
        print("5. IMPORT CITIES")
        print("6. IMPORT ROOM TYPES")
        print("7. IMPORT ROOMS")
        print("8. IMPORT DEPARTMENTS")
        print("9. IMPORT ALL DATA")
        print("0. EXIT")
        print("=" * 50)

        choice = input("\nSelect option (0-9): ")
        
        if choice == '1':
            print("\n" + "=" * 50)
            confirm = input("▲ Type 'YES' to confirm cleaning ALL data: ")
            if confirm.upper() == 'YES':
                clean_all_data()
            else:
                print("✗ Operation cancelled.")
        
        elif choice == '2':
            print("\n" + "=" * 40)
            confirm = input("▲ Type 'YES' to confirm cleaning all cities: ")
            if confirm.upper() == 'YES':
                clean_cities()
            else:
                print("✗ Operation cancelled.")
        
        elif choice == '3':
            print("\n" + "=" * 40)
            confirm = input("▲ Type 'YES' to confirm cleaning all room types: ")
            if confirm.upper() == 'YES':
                clean_room_types()
            else:
                print("✗ Operation cancelled.")
        
        elif choice == '4':
            print("\n" + "=" * 40)
            confirm = input("▲ Type 'YES' to confirm cleaning all rooms: ")
            if confirm.upper() == 'YES':
                clean_rooms()
            else:
                print("✗ Operation cancelled.")
        
        elif choice == '5':
            print("\n" + "=" * 40)
            import_cities_only()
        
        elif choice == '6':
            print("\n" + "=" * 40)
            import_room_types_only()
        
        elif choice == '7':
            print("\n" + "=" * 40)
            import_rooms_only()
        
        elif choice == '8':
            print("\n" + "=" * 40)
            import_departments_only()
        
        elif choice == '9':
            print("\n" + "=" * 50)
            import_all_data()
        
        elif choice == '0':
            print("\nThank you for using ABC Hotels! 🏨")
            break
        
        else:
            print("✗ Invalid choice!")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()