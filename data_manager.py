# data_manager.py
import os
import csv
import django
import sys

# Setup Django environment
sys.path.append('/Users/anita/abchotels')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abchotels.settings')  # FIXED: DJANGQ to DJANGO
django.setup()

from hotel.models import City, Department, RoomType, Room  # ADDED: Room

CSV_FOLDER = 'csv'
EXPORTS_FOLDER = 'exports'

def ensure_folder_exists(folder_name):
    """Create folder if it doesn't exist"""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def clean_all_data():
    """Clean all data from all models"""
    print("\n▲ WARNING: This will delete ALL data from the database!")
    confirmation = input("Are you sure you want to continue? (yes/no): ").lower()

    if confirmation == 'yes':
        try:
            Room.objects.all().delete()  # ADDED: Clean rooms first
            RoomType.objects.all().delete()
            Department.objects.all().delete()
            City.objects.all().delete()
            print("◄ All data has been successfully cleaned!")
        except Exception as e:
            print(f"✗ Error cleaning data: {e}")
    else:
        print("✗ Operation cancelled.")

def import_data():
    """Import all data from CSV files - handle duplicates properly"""
    print("\n$ Importing all data from CSV files...")

    # Check if CSV folder exists
    if not os.path.exists(CSV_FOLDER):
        print(f"✗ CSV folder '{CSV_FOLDER}' not found!")
        return

    # Import Cities
    print("\n$ Importing Cities...")
    try:
        filepath = os.path.join(CSV_FOLDER, 'cities.csv')
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            imported_count = 0
            updated_count = 0
            skipped_count = 0

            for row in reader:
                name = row.get('name', '').strip()
                if name:
                    is_active = row.get('is_active', 'True').lower() == 'true'

                    # Check for existing cities with same name
                    existing_cities = City.objects.filter(name=name)

                    if existing_cities.exists():
                        # Update all duplicates (keep first, delete others)
                        first_city = existing_cities.first()
                        first_city.is_active = is_active
                        first_city.save()

                        # Delete other duplicates
                        if existing_cities.count() > 1:
                            existing_cities.exclude(id=first_city.id).delete()  # FIXED: execute to exclude
                            print(f"▲ Removed duplicate cities for '{name}'")

                        updated_count += 1
                    else:
                        # Create new city
                        City.objects.create(name=name, is_active=is_active)
                        imported_count += 1

            print(f"☑ Cities: {imported_count} imported, {updated_count} updated, {skipped_count} skipped")

    except Exception as e:
        print(f"✗ Error importing cities: {e}")

    # Import Departments
    print("\n⇔ Importing Departments...")
    try:
        filepath = os.path.join(CSV_FOLDER, 'departments.csv')
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            imported_count = 0
            updated_count = 0
            skipped_count = 0

            for row in reader:
                name = row.get('name', '').strip()
                if name:
                    # Check for existing departments with same name
                    existing_depts = Department.objects.filter(name=name)

                    if existing_depts.exists():
                        # Keep only the first one, delete duplicates
                        if existing_depts.count() > 1:  # FIXED: existing_depts_count() to existing_depts.count()
                            first_dept = existing_depts.first()
                            existing_depts.exclude(id=first_dept.id).delete()
                            print(f"▲ Removed duplicate departments for '{name}'")
                        updated_count += 1
                    else:
                        # Create new department
                        Department.objects.create(name=name)
                        imported_count += 1

            print(f"◇ Departments: {imported_count} imported, {updated_count} updated, {skipped_count} skipped")

    except Exception as e:
        print(f"✗ Error importing departments: {e}")

    # Import Room Types
    print("\n⏿ Importing Room Types...")
    try:
        filepath = os.path.join(CSV_FOLDER, 'room_types.csv')
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            imported_count = 0
            updated_count = 0
            skipped_count = 0

            for row in reader:
                name = row.get('name', '').strip()
                if name:
                    try:
                        price = float(row.get('price_per_night', 0))
                        capacity = int(row.get('capacity', 1))
                        # Check for existing room types with same name
                        existing_rooms = RoomType.objects.filter(name=name)

                        if existing_rooms.exists():
                            # Update first one and delete duplicates
                            first_room = existing_rooms.first()
                            first_room.price_per_night = price
                            first_room.capacity = capacity
                            first_room.save()

                            # Delete other duplicates
                            if existing_rooms.count() > 1:
                                existing_rooms.exclude(id=first_room.id).delete()
                                print(f"▲ Removed duplicate room types for '{name}'")

                            updated_count += 1
                        else:
                            # Create new room type
                            RoomType.objects.create(
                                name=name,
                                price_per_night=price,
                                capacity=capacity
                            )
                            imported_count += 1
                    except ValueError:
                        print(f"▲ Skipping invalid row: {row}")
                        skipped_count += 1
                        continue

            print(f"◉ Room Types: {imported_count} imported, {updated_count} updated, {skipped_count} skipped")

    except Exception as e:
        print(f"✗ Error importing room types: {e}")

    # ADDED: Import Rooms
    print("\n🏨 Importing Rooms...")
    try:
        filepath = os.path.join(CSV_FOLDER, 'rooms.csv')
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            imported_count = 0
            skipped_count = 0

            for row in reader:
                city_name = row.get('city', '').strip()
                room_type_name = row.get('room_type', '').strip()
                is_available = row.get('is_available', 'True').lower() == 'true'

                if city_name and room_type_name:
                    try:
                        # Get city and room type objects
                        city = City.objects.get(name=city_name)
                        room_type = RoomType.objects.get(name=room_type_name)

                        # Create room
                        Room.objects.create(
                            city=city,
                            room_type=room_type,
                            is_available=is_available
                        )
                        imported_count += 1

                    except City.DoesNotExist:
                        print(f"▲ Skipping room - City '{city_name}' not found")
                        skipped_count += 1
                    except RoomType.DoesNotExist:
                        print(f"▲ Skipping room - Room Type '{room_type_name}' not found")
                        skipped_count += 1
                    except Exception as e:
                        print(f"▲ Error creating room: {e}")
                        skipped_count += 1
                else:
                    skipped_count += 1

            print(f"🏨 Rooms: {imported_count} imported, {skipped_count} skipped")

    except FileNotFoundError:
        print("ℹ Rooms CSV file not found, skipping rooms import")
    except Exception as e:
        print(f"✗ Error importing rooms: {e}")

def export_data():
    """Export all data to CSV files with simple 'export' prefix"""
    print("\n📤 Exporting all data to CSV files...")
    ensure_folder_exists(EXPORTS_FOLDER)

    # Export Cities
    try:
        filename = os.path.join(EXPORTS_FOLDER, 'export_cities.csv')
        cities = City.objects.all()
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'is_active'])
            for city in cities:
                writer.writerow([city.name, city.is_active])
        print(f"📌 Exported {cities.count()} cities to {filename}")
    except Exception as e:
        print(f"✗ Error exporting cities: {e}")

    # Export Departments
    try:
        filename = os.path.join(EXPORTS_FOLDER, 'export_departments.csv')
        departments = Department.objects.all()
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name'])
            for dept in departments:
                writer.writerow([dept.name])
        print(f"📌 Exported {departments.count()} departments to {filename}")
    except Exception as e:
        print(f"✗ Error exporting departments: {e}")

    # Export Room Types
    try:
        filename = os.path.join(EXPORTS_FOLDER, 'export_room_types.csv')
        room_types = RoomType.objects.all()
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'price_per_night', 'capacity'])
            for room_type in room_types:
                writer.writerow([room_type.name, room_type.price_per_night, room_type.capacity])
        print(f"📌 Exported {room_types.count()} room types to {filename}")
    except Exception as e:
        print(f"✗ Error exporting room types: {e}")

    # ADDED: Export Rooms
    try:
        filename = os.path.join(EXPORTS_FOLDER, 'export_rooms.csv')
        rooms = Room.objects.all().select_related('city', 'room_type')
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['city', 'room_type', 'is_available'])
            for room in rooms:
                writer.writerow([room.city.name, room.room_type.name, room.is_available])
        print(f"📌 Exported {rooms.count()} rooms to {filename}")
    except Exception as e:
        print(f"✗ Error exporting rooms: {e}")

def show_database_summary():
    """Show current database counts"""
    print(f"\n📊 Current Database Summary:")
    print(f"  Cities: {City.objects.count()}")
    print(f"  Departments: {Department.objects.count()}")
    print(f"  Room Types: {RoomType.objects.count()}")
    print(f"  Rooms: {Room.objects.count()}")  # ADDED: Rooms count

def main():
    """Main program loop"""
    ensure_folder_exists(CSV_FOLDER)
    ensure_folder_exists(EXPORTS_FOLDER)

    while True:
        print("\n" + "="*50)
        print("🟩 ABC Hotels - Data Manager")
        print("="*50)
        show_database_summary()
        print("="*50)
        print("1. Clean All Data")
        print("2. Import Data")
        print("3. Export Data")
        print("4. Exit")
        print("="*50)

        choice = input("\nSelect option (1-4): ")
        if choice == '1':
            clean_all_data()
        elif choice == '2':
            import_data()
        elif choice == '3':
            export_data()
        elif choice == '4':
            print("💬 Thank you for using ABC Hotels Data Manager!")
            break
        else:
            print("✗ Invalid choice! Please select 1-4.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()