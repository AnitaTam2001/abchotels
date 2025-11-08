# import.py (Final Complete Version)
import os
import sys
import django
import csv
import time
from datetime import datetime

# Setup Django environment
sys.path.append('/Users/anita/abchotels')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abchotels.settings')
django.setup()

from django.db import connection
from hotel.models import City, RoomType, Room, Department, Booking, FAQ, JobListing, JobApplication

CSV_FOLDER = 'csv'  # Folder where CSV files are located

def close_db_connection():
    """Explicitly close database connection to prevent locking"""
    try:
        connection.close()
        time.sleep(0.05)
    except Exception as e:
        print(f"⚠️  Could not close database connection: {e}")

def create_all_csv_files():
    """Create all necessary CSV files for complete hotel setup"""
    print("📁 Creating all CSV files...")
    
    # 1. Create Cities CSV
    cities_data = """ID,Name,Description,Is Active,Image Filename
1,New York,"The vibrant heart of America with iconic landmarks",true,cities/new_york.jpg
2,London,"Historic capital with royal palaces and modern attractions",true,cities/london.jpg
3,Paris,"City of Light with romantic ambiance and art",true,cities/paris.jpg
4,Tokyo,"Bustling metropolis blending tradition and technology",true,cities/tokyo.jpg
5,Dubai,"Luxury destination with stunning architecture",true,cities/dubai.jpg
6,Singapore,"Clean, green city with diverse cultures",true,cities/singapore.jpg
7,Sydney,"Harbor city with iconic opera house and beaches",true,cities/sydney.jpg
8,Rome,"Eternal city with ancient history and cuisine",true,cities/rome.jpg
9,Barcelona,"Artistic city with unique architecture and beaches",true,cities/barcelona.jpg
10,Bangkok,"Vibrant city with temples and street food",true,cities/bangkok.jpg
11,Los Angeles,"Entertainment capital with sunny beaches",true,cities/los_angeles.jpg
12,Amsterdam,"Canal city with museums and cycling culture",true,cities/amsterdam.jpg
13,Istanbul,"Cross-continental city rich in history",true,cities/istanbul.jpg
14,Hong Kong,"Skyscraper-filled city with mountain views",true,cities/hong_kong.jpg
15,Miami,"Art deco beauty with vibrant nightlife",true,cities/miami.jpg
16,Prague,"Medieval charm with stunning architecture",true,cities/prague.jpg
17,Vienna,"Imperial city of music and coffee houses",true,cities/vienna.jpg
18,Kyoto,"Traditional Japanese city with temples and gardens",true,cities/kyoto.jpg
"""
    
    with open(os.path.join(CSV_FOLDER, 'import_city.csv'), 'w', encoding='utf-8') as file:
        file.write(cities_data)
    print("✅ Created cities CSV")
    
    # 2. Create Room Types CSV (using only available JPG images)
    roomtypes_data = """ID,Name,Description,Price Per Night,Capacity,Image Filename
1,Accessible King,ADA compliant room with roll-in shower and grab bars,169.00,2,rooms/accessible_king.jpg
2,Junior Suite,Compact suite with small living area,279.00,2,rooms/junior_suite.jpg
3,Pool View King,King room with direct pool access and view,229.00,2,rooms/junior_suite.jpg
4,City View Twin,Twin beds with panoramic city views,189.00,2,rooms/cityview_twin.jpg
5,Corner Suite,Spacious corner room with extra windows,329.00,3,rooms/corner_suite.jpg
6,Studio King,Open concept room with kitchenette,219.00,2,rooms/studio_king.jpg
7,Connecting Family,Two connecting rooms perfect for larger families,499.00,6,rooms/connecting_family.jpg
8,Garden View Queen,Peaceful room overlooking hotel gardens,179.00,2,rooms/garden_queen.jpg
9,Penthouse Suite,Top-floor suite with private balcony,799.00,4,rooms/penthouse_suite.jpg
"""
    
    with open(os.path.join(CSV_FOLDER, 'import_roomtype.csv'), 'w', encoding='utf-8') as file:
        file.write(roomtypes_data)
    print("✅ Created room types CSV")
    
    # 3. Create Departments CSV
    departments_data = """ID,Name,Description
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
    
    with open(os.path.join(CSV_FOLDER, 'import_department.csv'), 'w', encoding='utf-8') as file:
        file.write(departments_data)
    print("✅ Created departments CSV")
    
    # 4. Create Rooms CSV
    rooms_data = """ID,City ID,Room Type ID,Is Available
101,1,1,true
102,1,1,true
103,1,2,true
104,1,2,true
105,1,3,true
106,1,3,true
107,1,4,true
108,1,4,true
109,1,5,true
110,1,5,true
111,1,6,true
112,1,6,true
113,1,7,true
114,1,8,true
115,1,8,true
116,1,9,true
201,2,1,true
202,2,1,true
203,2,2,true
204,2,3,true
205,2,4,true
206,2,5,true
207,2,6,true
208,2,8,true
209,2,9,true
301,3,1,true
302,3,2,true
303,3,3,true
304,3,4,true
305,3,5,true
306,3,6,true
307,3,8,true
308,3,9,true
401,4,1,true
402,4,1,true
403,4,2,true
404,4,3,true
405,4,4,true
406,4,6,true
407,4,8,true
501,5,1,true
502,5,2,true
503,5,3,true
504,5,5,true
505,5,6,true
506,5,9,true
"""
    
    with open(os.path.join(CSV_FOLDER, 'import_room.csv'), 'w', encoding='utf-8') as file:
        file.write(rooms_data)
    print("✅ Created rooms CSV")
    
    print("🎉 All CSV files created successfully!")
    return True

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
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                return 0
                
            cities_created = 0
            for row in reader:
                defaults = {
                    'name': row['Name'],
                    'description': row['Description'],
                    'is_active': row['Is Active'].lower() == 'true',
                    'image': row['Image Filename']
                }
                
                city, created = City.objects.get_or_create(
                    id=row['ID'],
                    defaults=defaults
                )
                
                if created:
                    cities_created += 1
                
                close_db_connection()
            
            print(f"✅ Cities: {cities_created} created")
            return cities_created
            
    except Exception as e:
        print(f"❌ Error importing cities: {e}")
        return 0

def import_roomtype(filename):
    """Import RoomType data from CSV"""
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                return 0
                
            roomtypes_created = 0
            for row in reader:
                defaults = {
                    'name': row['Name'],
                    'description': row['Description'],
                    'price_per_night': float(row['Price Per Night']),
                    'capacity': int(row['Capacity']),
                    'image': row['Image Filename']
                }
                
                roomtype, created = RoomType.objects.get_or_create(
                    id=row['ID'],
                    defaults=defaults
                )
                
                if created:
                    roomtypes_created += 1
                    print(f"  ✅ {row['Name']}")
                
                close_db_connection()
            
            print(f"✅ Room Types: {roomtypes_created} created")
            return roomtypes_created
            
    except Exception as e:
        print(f"❌ Error importing room types: {e}")
        return 0

def import_department(filename):
    """Import Department data from CSV"""
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                return 0
                
            departments_created = 0
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
                
                close_db_connection()
            
            print(f"✅ Departments: {departments_created} created")
            return departments_created
            
    except Exception as e:
        print(f"❌ Error importing departments: {e}")
        return 0

def import_room(filename):
    """Import Room data from CSV"""
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = skip_comments_and_get_reader(file)
            if not reader:
                return 0
                
            rooms_created = 0
            missing_refs = 0
            
            for row in reader:
                try:
                    city = City.objects.get(id=row['City ID'])
                    room_type = RoomType.objects.get(id=row['Room Type ID'])
                    
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
                
                except (City.DoesNotExist, RoomType.DoesNotExist):
                    missing_refs += 1
                
                close_db_connection()
            
            print(f"✅ Rooms: {rooms_created} created")
            if missing_refs > 0:
                print(f"⚠️  Skipped {missing_refs} rooms due to missing references")
            return rooms_created
            
    except Exception as e:
        print(f"❌ Error importing rooms: {e}")
        return 0

def import_all_data():
    """Import all data to set up complete hotel system"""
    print("🚀 IMPORTING ALL HOTEL DATA...")
    print("=" * 50)
    
    # Create all CSV files first
    if not create_all_csv_files():
        print("❌ Failed to create CSV files")
        return False
    
    total_records = 0
    
    # Import in correct order
    import_steps = [
        ("🌆 Cities", "import_city.csv", import_city),
        ("🏨 Room Types", "import_roomtype.csv", import_roomtype),
        ("🏢 Departments", "import_department.csv", import_department),
        ("🛏️ Rooms", "import_room.csv", import_room),
    ]
    
    for step_name, filename, import_func in import_steps:
        print(f"\n📥 Importing {step_name}...")
        records = import_func(filename)
        total_records += records
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("🎉 IMPORT COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    
    # Show final database state
    print("\n📊 FINAL DATABASE STATE:")
    print(f"   🌆 Cities: {City.objects.count()}")
    print(f"   🏨 Room Types: {RoomType.objects.count()}")
    print(f"   🛏️ Rooms: {Room.objects.count()}")
    print(f"   🏢 Departments: {Department.objects.count()}")
    print(f"   📈 Total Records: {total_records}")
    
    # Verify room types
    print(f"\n🔍 VERIFYING ROOM TYPES:")
    roomtypes = RoomType.objects.all().order_by('id')
    for roomtype in roomtypes:
        image_exists = os.path.exists(os.path.join('static/images/', roomtype.image.name)) if roomtype.image else False
        status = "✅" if image_exists else "❌"
        print(f"   {status} {roomtype.id}. {roomtype.name} - {roomtype.image.name if roomtype.image else 'No image'}")
    
    print(f"\n✨ Your ABC Hotels system is now fully set up!")
    print("   You can start the Django server and access the admin panel.")
    
    return True

def clean_all_data():
    """Clean all data from database"""
    print("🧹 CLEANING ALL DATA...")
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
        print(f"🗑️  {model_name}: {count} deleted")
        total_deleted += count
        time.sleep(0.1)
    
    print("=" * 50)
    print(f"✅ All data cleaned! {total_deleted} total records deleted")
    return True

def show_current_state():
    """Show current database state"""
    print("\n📊 CURRENT DATABASE STATE:")
    print(f"   🌆 Cities: {City.objects.count()}")
    print(f"   🏨 Room Types: {RoomType.objects.count()}")
    print(f"   🛏️ Rooms: {Room.objects.count()}")
    print(f"   🏢 Departments: {Department.objects.count()}")
    print(f"   📋 FAQs: {FAQ.objects.count()}")
    print(f"   💼 Job Listings: {JobListing.objects.count()}")
    print(f"   📝 Job Applications: {JobApplication.objects.count()}")
    print(f"   🏷️ Bookings: {Booking.objects.count()}")

def main():
    """Main program loop"""
    # Ensure CSV folder exists
    if not os.path.exists(CSV_FOLDER):
        os.makedirs(CSV_FOLDER)
    
    while True:
        print("\n" + "="*50)
        print("   🏨 ABC HOTELS - COMPLETE SETUP MANAGER")
        print("="*50)
        
        show_current_state()
        
        print("="*50)
        print("1. 🚀 IMPORT ALL DATA (Complete Setup)")
        print("2. 🧹 CLEAN ALL DATA (Start Fresh)")
        print("3. 📋 SHOW CURRENT STATE")
        print("4. 🚪 EXIT")
        print("="*50)

        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            import_all_data()
        elif choice == '2':
            clean_all_data()
        elif choice == '3':
            show_current_state()
        elif choice == '4':
            print("👋 Thank you for using ABC Hotels Setup Manager!")
            break
        else:
            print("❌ Invalid choice! Please select 1-4.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'import-all':
        import_all_data()
    elif len(sys.argv) > 1 and sys.argv[1] == 'clean':
        clean_all_data()
    else:
        main()