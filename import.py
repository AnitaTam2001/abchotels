# import.py (with corrected image paths)
import os
import sys
import django
import csv
from datetime import datetime

# Setup Django environment
sys.path.append('/Users/anita/abchotels')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abchotels.settings')
django.setup()

from hotel.models import City, RoomType, Room, Department, Booking, FAQ, JobListing, JobApplication

CSV_FOLDER = 'csv'  # Folder where CSV files are located

def clean_all_data():
    """
    Delete all data from all models to start fresh
    """
    print("🧹 Cleaning all data from database...")
    print("=" * 50)
    
    try:
        # Store counts before deletion
        city_count = City.objects.count()
        roomtype_count = RoomType.objects.count()
        room_count = Room.objects.count()
        department_count = Department.objects.count()
        booking_count = Booking.objects.count()
        faq_count = FAQ.objects.count()
        joblisting_count = JobListing.objects.count()
        jobapplication_count = JobApplication.objects.count()
        
        # Delete in correct order to respect foreign key constraints
        print("🗑️  Deleting bookings...")
        Booking.objects.all().delete()
        
        print("🗑️  Deleting job applications...")
        JobApplication.objects.all().delete()
        
        print("🗑️  Deleting job listings...")
        JobListing.objects.all().delete()
        
        print("🗑️  Deleting FAQs...")
        FAQ.objects.all().delete()
        
        print("🗑️  Deleting rooms...")
        Room.objects.all().delete()
        
        print("🗑️  Deleting room types...")
        RoomType.objects.all().delete()
        
        print("🗑️  Deleting departments...")
        Department.objects.all().delete()
        
        print("🗑️  Deleting cities...")
        City.objects.all().delete()
        
        print("=" * 50)
        print("✅ All data cleaned successfully!")
        print(f"📊 Records deleted:")
        print(f"   Cities: {city_count}")
        print(f"   Room Types: {roomtype_count}")
        print(f"   Rooms: {room_count}")
        print(f"   Departments: {department_count}")
        print(f"   Bookings: {booking_count}")
        print(f"   FAQs: {faq_count}")
        print(f"   Job Listings: {joblisting_count}")
        print(f"   Job Applications: {jobapplication_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning data: {e}")
        import traceback
        traceback.print_exc()
        return False

def ensure_folder_exists(folder_name):
    """Create folder if it doesn't exist"""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def skip_comments_and_get_reader(file):
    """Skip comment lines and return CSV reader with proper header"""
    lines = []
    for line in file:
        # Skip lines that start with # (comments)
        if not line.strip().startswith('#'):
            lines.append(line)
    
    # Create CSV reader from non-comment lines
    if lines:
        return csv.DictReader(lines)
    else:
        return None

def create_department_csv():
    """Create the correct department CSV file since it's missing"""
    department_data = """ID,Name,Description
1,Front Office,"Manages guest services, reservations, and front desk operations"
2,Housekeeping,"Responsible for room cleaning and maintenance"
3,Food and Beverage,"Manages restaurants, bars, and room service"
4,Sales and Marketing,"Handles promotions, partnerships, and business development"
5,Human Resources,"Manages recruitment, training, and employee relations"
6,Finance,"Handles accounting, budgeting, and financial reporting"
7,Maintenance,"Responsible for property upkeep and repairs"
8,Security,"Ensures guest safety and property security"
9,Events and Catering,"Manages conferences, weddings, and special events"
10,Spa and Wellness,"Operates spa, fitness center, and wellness programs"
"""
    
    filepath = os.path.join(CSV_FOLDER, 'import_department.csv')
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(department_data)
    print(f"✅ Created missing department CSV file: {filepath}")
    return True

def create_missing_roomtypes():
    """Create missing room types for IDs 21-40"""
    print("🔧 Creating missing room types (IDs 21-40)...")
    
    # Extended room types data for IDs 21-40
    extended_roomtypes = [
        (21, "Family Connector", "Connecting rooms perfect for families", 598.00, 6, "rooms/family_connector.png"),
        (22, "Presidential Corner", "Corner presidential suite with panoramic views", 899.00, 4, "rooms/presidential_corner.png"),
        (23, "Royal Suite", "Ultimate luxury with royal treatment", 1299.00, 4, "rooms/royal_suite.png"),
        (24, "Panoramic Suite", "Suite with breathtaking panoramic city views", 759.00, 3, "rooms/panoramic_suite.png"),
        (25, "Bi-Level Suite", "Two-level suite with separate living areas", 899.00, 4, "rooms/bi_level_suite.png"),
        (26, "Penthouse Suite", "Top-floor penthouse with exclusive amenities", 1199.00, 4, "rooms/penthouse_suite.png"),
        (27, "Artist Loft", "Creative space with artistic decor", 429.00, 2, "rooms/artist_loft.png"),
        (28, "Wellness Room", "Room focused on health and wellness features", 329.00, 2, "rooms/wellness_room.png"),
        (29, "Quiet Zone King", "Soundproof room for maximum tranquility", 179.00, 2, "rooms/quiet_zone_king.png"),
        (30, "Allergy Free King", "Hypoallergenic room for sensitive guests", 199.00, 2, "rooms/allergy_free_king.png"),
        (31, "Pet Friendly King", "Room designed for guests with pets", 189.00, 2, "rooms/pet_friendly_king.png"),
        (32, "Extended Stay Suite", "Suite with kitchenette for long-term stays", 379.00, 3, "rooms/extended_stay_suite.png"),
        (33, "Club Level King", "King room with exclusive club access", 319.00, 2, "rooms/club_level_king.png"),
        (34, "Club Level Suite", "Suite with exclusive club level privileges", 549.00, 3, "rooms/club_level_suite.png"),
        (35, "Terrace Suite", "Suite with private outdoor terrace", 679.00, 3, "rooms/terrace_suite.png"),
        (36, "Courtyard View King", "King room overlooking peaceful courtyard", 159.00, 2, "rooms/courtyard_view_king.png"),
        (37, "Historic Room", "Room preserving historical architectural elements", 229.00, 2, "rooms/historic_room.png"),
        (38, "Modern Loft", "Contemporary loft-style accommodation", 389.00, 2, "rooms/modern_loft.png"),
        (39, "Traditional Room", "Classic decor with traditional furnishings", 169.00, 2, "rooms/traditional_room.png"),
        (40, "Contemporary King", "Modern king room with sleek design", 209.00, 2, "rooms/contemporary_king.png")
    ]
    
    created_count = 0
    for roomtype_id, name, description, price, capacity, image in extended_roomtypes:
        roomtype, created = RoomType.objects.update_or_create(
            id=roomtype_id,
            defaults={
                'name': name,
                'description': description,
                'price_per_night': price,
                'capacity': capacity,
                'image': image
            }
        )
        if created:
            created_count += 1
    
    print(f"✅ Created {created_count} missing room types")
    return created_count

def import_city(filename):
    """
    Import City data from CSV with corrected image paths
    """
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                print(f"❌ No data found in {filename}")
                return 0
                
            cities_created = 0
            cities_updated = 0
            
            for row in reader:
                city_id = row['ID']
                
                # Handle image path - ensure it's in cities folder
                image_filename = row['Image Filename'] if row['Image Filename'] else None
                if image_filename and not image_filename.startswith('cities/'):
                    image_filename = f"cities/{image_filename}"
                
                defaults = {
                    'name': row['Name'],
                    'description': row['Description'],
                    'is_active': row['Is Active'].lower() == 'true',
                    'image': image_filename
                }
                
                city, created = City.objects.update_or_create(
                    id=city_id,
                    defaults=defaults
                )
                
                if created:
                    cities_created += 1
                else:
                    cities_updated += 1
            
            print(f"✅ Cities: {cities_created} created, {cities_updated} updated")
            return cities_created + cities_updated
            
    except Exception as e:
        print(f"❌ Error importing cities: {e}")
        import traceback
        traceback.print_exc()
        return 0

def import_roomtype(filename):
    """
    Import RoomType data from CSV with corrected image paths
    """
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                print(f"❌ No data found in {filename}")
                return 0
                
            roomtypes_created = 0
            roomtypes_updated = 0
            
            for row in reader:
                roomtype_id = row['ID']
                
                # Handle image path - ensure it's in rooms folder
                image_filename = row['Image Filename'] if row['Image Filename'] else None
                if image_filename and not image_filename.startswith('rooms/'):
                    image_filename = f"rooms/{image_filename}"
                
                defaults = {
                    'name': row['Name'],
                    'description': row['Description'],
                    'price_per_night': float(row['Price Per Night']),
                    'capacity': int(row['Capacity']),
                    'image': image_filename
                }
                
                roomtype, created = RoomType.objects.update_or_create(
                    id=roomtype_id,
                    defaults=defaults
                )
                
                if created:
                    roomtypes_created += 1
                else:
                    roomtypes_updated += 1
            
            print(f"✅ Room Types: {roomtypes_created} created, {roomtypes_updated} updated")
            return roomtypes_created + roomtypes_updated
            
    except Exception as e:
        print(f"❌ Error importing room types: {e}")
        import traceback
        traceback.print_exc()
        return 0

def import_room(filename):
    """
    Import Room data from CSV
    """
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                print(f"❌ No data found in {filename}")
                return 0
                
            rooms_created = 0
            rooms_updated = 0
            missing_roomtypes = set()
            
            for row in reader:
                room_id = row['ID']
                
                # Get related objects
                try:
                    city = City.objects.get(id=row['City ID'])
                except City.DoesNotExist:
                    print(f"❌ City with ID {row['City ID']} not found, skipping room {room_id}")
                    continue
                
                try:
                    room_type = RoomType.objects.get(id=row['Room Type ID'])
                except RoomType.DoesNotExist:
                    missing_roomtypes.add(row['Room Type ID'])
                    print(f"❌ Room Type with ID {row['Room Type ID']} not found, skipping room {room_id}")
                    continue
                
                # Only use fields that exist in the Room model
                defaults = {
                    'city': city,
                    'room_type': room_type,
                    'is_available': row['Is Available'].lower() == 'true'
                }
                
                room, created = Room.objects.update_or_create(
                    id=room_id,
                    defaults=defaults
                )
                
                if created:
                    rooms_created += 1
                else:
                    rooms_updated += 1
            
            # Report on missing room types
            if missing_roomtypes:
                print(f"⚠️  Missing room types detected: {sorted(missing_roomtypes)}")
                print("💡 Use option 10 to create missing room types")
            
            print(f"✅ Rooms: {rooms_created} created, {rooms_updated} updated")
            return rooms_created + rooms_updated
            
    except Exception as e:
        print(f"❌ Error importing rooms: {e}")
        import traceback
        traceback.print_exc()
        return 0

def import_department(filename):
    """
    Import Department data from CSV
    """
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        
        # Check if file needs to be recreated
        needs_recreation = False
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as test_file:
                first_line = test_file.readline().strip()
                # If it doesn't start with proper CSV headers, recreate it
                if not first_line.startswith('ID,Name,Description') and not first_line.startswith('#'):
                    needs_recreation = True
        
        if not os.path.exists(filepath) or needs_recreation:
            print(f"⚠️  {filename} is missing or corrupted. Creating proper CSV file...")
            create_department_csv()
            filepath = os.path.join(CSV_FOLDER, 'import_department.csv')
        
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                print(f"❌ No data found in {filename}")
                return 0
                
            departments_created = 0
            departments_updated = 0
            
            for row in reader:
                # Validate that we have the required fields
                if 'ID' not in row:
                    print(f"❌ Missing 'ID' field in department CSV")
                    print(f"Available fields: {list(row.keys())}")
                    return 0
                    
                department_id = row['ID']
                defaults = {
                    'name': row['Name'],
                    'description': row['Description']
                }
                
                department, created = Department.objects.update_or_create(
                    id=department_id,
                    defaults=defaults
                )
                
                if created:
                    departments_created += 1
                else:
                    departments_updated += 1
            
            print(f"✅ Departments: {departments_created} created, {departments_updated} updated")
            return departments_created + departments_updated
            
    except Exception as e:
        print(f"❌ Error importing departments: {e}")
        print(f"💡 Try using option 8 to recreate the department CSV file")
        import traceback
        traceback.print_exc()
        return 0

def check_csv_files():
    """
    Check if all required CSV files exist in the csv folder
    """
    required_files = [
        'import_city.csv',
        'import_roomtype.csv', 
        'import_room.csv',
        'import_department.csv'
    ]
    
    missing_files = []
    
    for filename in required_files:
        filepath = os.path.join(CSV_FOLDER, filename)
        if not os.path.exists(filepath):
            missing_files.append(filename)
    
    if missing_files:
        print("❌ Missing CSV files in 'csv' folder:")
        for filename in missing_files:
            print(f"   - {filename}")
        return False
    else:
        print("✅ All required CSV files found in 'csv' folder!")
        return True

def import_all():
    """
    Import all data from CSV files in csv folder
    """
    if not check_csv_files():
        print("\n💡 Please make sure all CSV files are in the 'csv' folder:")
        print("   - import_city.csv")
        print("   - import_roomtype.csv")
        print("   - import_room.csv") 
        print("   - import_department.csv")
        return 0
    
    print("🚀 Starting import of all data...")
    print("=" * 50)
    
    total_records = 0
    
    # Import in correct order to maintain foreign key relationships
    files_to_import = [
        ('import_city.csv', import_city),
        ('import_roomtype.csv', import_roomtype),
        ('import_department.csv', import_department),  # Import departments before rooms
        ('import_room.csv', import_room),
    ]
    
    for filename, import_function in files_to_import:
        print(f"\n📥 Importing {filename}...")
        records = import_function(filename)
        total_records += records
    
    # Create missing room types if needed
    print(f"\n🔧 Checking for missing room types...")
    create_missing_roomtypes()
    
    print(f"\n🎉 Import completed! {total_records} total records processed.")
    
    # Display final counts
    print("\n📊 Final Database Counts:")
    print(f"   Cities: {City.objects.count()}")
    print(f"   Room Types: {RoomType.objects.count()}")
    print(f"   Rooms: {Room.objects.count()}")
    print(f"   Departments: {Department.objects.count()}")
    
    return total_records

def show_csv_files():
    """Show available CSV files in csv folder"""
    ensure_folder_exists(CSV_FOLDER)
    
    files = os.listdir(CSV_FOLDER)
    csv_files = [f for f in files if f.endswith('.csv')]
    
    print(f"\n📁 Available CSV files in '{CSV_FOLDER}':")
    for file in csv_files:
        filepath = os.path.join(CSV_FOLDER, file)
        file_size = os.path.getsize(filepath)
        print(f"   📄 {file} ({file_size} bytes)")
    
    return csv_files

def debug_csv_file(filename):
    """Debug function to check CSV file structure"""
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        print(f"\n🔍 Debugging {filename}:")
        print(f"File exists: {os.path.exists(filepath)}")
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                print(f"Total lines: {len(lines)}")
                print("First 10 lines:")
                for i, line in enumerate(lines[:10]):
                    print(f"  {i+1}: {line.strip()}")
                
                # Test the CSV reader
                file.seek(0)
                reader = skip_comments_and_get_reader(file)
                if reader:
                    print(f"CSV headers: {reader.fieldnames}")
                    # Show first few data rows
                    try:
                        for i, row in enumerate(reader):
                            if i < 3:  # Show first 3 data rows
                                print(f"Data row {i+1}: {dict(row)}")
                            else:
                                break
                    except StopIteration:
                        print("No data rows found")
                else:
                    print("No valid CSV data found")
    except Exception as e:
        print(f"Error debugging {filename}: {e}")

def main():
    """Main program loop"""
    ensure_folder_exists(CSV_FOLDER)
    
    while True:
        print("\n" + "="*50)
        print("   ABC Hotels - CSV Import Manager")
        print("="*50)
        
        # Show current database counts
        print(f"📊 Current Database:")
        print(f"   Cities: {City.objects.count()}")
        print(f"   Room Types: {RoomType.objects.count()}")
        print(f"   Rooms: {Room.objects.count()}")
        print(f"   Departments: {Department.objects.count()}")
        
        print("="*50)
        show_csv_files()
        print("="*50)
        print("1. Clean All Data (Start Fresh)")
        print("2. Import City")
        print("3. Import Room Type")
        print("4. Import Room")
        print("5. Import Department")
        print("6. Import All")
        print("7. Check CSV Files")
        print("8. Debug CSV Files")
        print("9. Fix Department CSV")
        print("10. Create Missing Room Types (21-40)")
        print("11. Exit")
        print("="*50)

        choice = input("\nSelect option (1-11): ").strip()
        
        if choice == '1':
            clean_all_data()
        elif choice == '2':
            import_city("import_city.csv")
        elif choice == '3':
            import_roomtype("import_roomtype.csv")
        elif choice == '4':
            import_room("import_room.csv")
        elif choice == '5':
            import_department("import_department.csv")
        elif choice == '6':
            import_all()
        elif choice == '7':
            check_csv_files()
        elif choice == '8':
            filename = input("Enter CSV filename to debug: ").strip()
            debug_csv_file(filename)
        elif choice == '9':
            create_department_csv()
        elif choice == '10':
            create_missing_roomtypes()
        elif choice == '11':
            print("👋 Thank you for using ABC Hotels Import Manager!")
            break
        else:
            print("❌ Invalid choice! Please select 1-11.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'all':
        # Command line mode - import all
        import_all()
    elif len(sys.argv) > 1 and sys.argv[1] == 'debug':
        # Debug mode
        if len(sys.argv) > 2:
            debug_csv_file(sys.argv[2])
        else:
            print("Usage: python import.py debug <filename>")
    elif len(sys.argv) > 1 and sys.argv[1] == 'clean':
        # Clean mode
        clean_all_data()
    else:
        # Interactive mode
        main()