# export.py (updated for simplified room format)
import os
import sys
import django
import csv

# Setup Django environment
sys.path.append('/Users/anita/abchotels')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abchotels.settings')
django.setup()

from hotel.models import City, RoomType, Room, Department

EXPORTS_FOLDER = 'exports'

def ensure_folder_exists(folder_name):
    """Create folder if it doesn't exist"""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def get_image_filename(instance, image_field):
    """
    Get image filename if it exists
    """
    image = getattr(instance, image_field)
    if image and hasattr(image, 'name'):
        return os.path.basename(image.name)
    return ""

def export_city():
    """
    Export all City data to CSV
    """
    ensure_folder_exists(EXPORTS_FOLDER)
    filename = os.path.join(EXPORTS_FOLDER, 'export_city.csv')
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Description', 'Is Active', 'Image Filename'])
        
        cities = City.objects.all()
        for city in cities:
            image_filename = get_image_filename(city, 'image')
            writer.writerow([
                city.id,
                city.name,
                city.description,
                city.is_active,
                image_filename
            ])
    
    print(f"✅ Exported {cities.count()} cities to {filename}")
    return filename

def export_roomtype():
    """
    Export all RoomType data to CSV
    """
    ensure_folder_exists(EXPORTS_FOLDER)
    filename = os.path.join(EXPORTS_FOLDER, 'export_roomtype.csv')
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Description', 'Price Per Night', 'Capacity', 'Image Filename'])
        
        room_types = RoomType.objects.all()
        for room_type in room_types:
            image_filename = get_image_filename(room_type, 'image')
            writer.writerow([
                room_type.id,
                room_type.name,
                room_type.description,
                room_type.price_per_night,
                room_type.capacity,
                image_filename
            ])
    
    print(f"✅ Exported {room_types.count()} room types to {filename}")
    return filename

def export_room():
    """
    Export all Room data to CSV (updated for simplified format)
    """
    ensure_folder_exists(EXPORTS_FOLDER)
    filename = os.path.join(EXPORTS_FOLDER, 'export_room.csv')
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'City ID', 'Room Type ID', 'Is Available', 'View Type', 'Price Per Night', 'Capacity', 'RoomType Image'])
        
        rooms = Room.objects.all().select_related('city', 'room_type')
        for room in rooms:
            writer.writerow([
                room.id,
                room.city.id if room.city else '',
                room.room_type.id if room.room_type else '',
                room.is_available,
                room.view_type,
                room.price_per_night,
                room.capacity,
                room.room_type_image
            ])
    
    print(f"✅ Exported {rooms.count()} rooms to {filename}")
    return filename

def export_department():
    """
    Export all Department data to CSV
    """
    ensure_folder_exists(EXPORTS_FOLDER)
    filename = os.path.join(EXPORTS_FOLDER, 'export_department.csv')
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Description'])
        
        departments = Department.objects.all()
        for department in departments:
            writer.writerow([
                department.id,
                department.name,
                department.description
            ])
    
    print(f"✅ Exported {departments.count()} departments to {filename}")
    return filename

def export_all():
    """
    Export all data (city, roomtype, room, department) to separate CSV files
    """
    ensure_folder_exists(EXPORTS_FOLDER)
    
    print("🚀 Starting export of all data...")
    
    # Export each dataset
    files = [
        export_city(),
        export_roomtype(),
        export_room(),
        export_department()
    ]
    
    print("🎉 All exports completed successfully!")
    return files

def show_database_summary():
    """Show current database counts"""
    print(f"\n📊 Current Database Summary:")
    print(f"   Cities: {City.objects.count()}")
    print(f"   Departments: {Department.objects.count()}")
    print(f"   Room Types: {RoomType.objects.count()}")
    print(f"   Rooms: {Room.objects.count()}")

def run_export(export_type='all'):
    """
    Run export from command line
    Usage: python export.py [export_type]
    export_type: city, roomtype, room, department, all
    """
    exports = {
        'city': export_city,
        'roomtype': export_roomtype,
        'room': export_room,
        'department': export_department,
        'all': export_all
    }
    
    show_database_summary()
    
    if export_type in exports:
        print(f"\n📤 Exporting {export_type}...")
        result = exports[export_type]()
        
        if export_type == 'all':
            print(f"\n🎉 All exports completed! Check the '{EXPORTS_FOLDER}' folder.")
        else:
            print(f"✅ Export completed: {result}")
    else:
        print(f"❌ Invalid export type: {export_type}")
        print("   Available types: city, roomtype, room, department, all")

def main():
    """Main program loop"""
    ensure_folder_exists(EXPORTS_FOLDER)
    
    while True:
        print("\n" + "="*50)
        print("   ABC Hotels - CSV Export Manager")
        print("="*50)
        show_database_summary()
        print("="*50)
        print("1. Export City")
        print("2. Export Room Type")
        print("3. Export Room")
        print("4. Export Department")
        print("5. Export All")
        print("6. Exit")
        print("="*50)

        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            export_city()
        elif choice == '2':
            export_roomtype()
        elif choice == '3':
            export_room()
        elif choice == '4':
            export_department()
        elif choice == '5':
            export_all()
        elif choice == '6':
            print("👋 Thank you for using ABC Hotels Export Manager!")
            break
        else:
            print("❌ Invalid choice! Please select 1-6.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        run_export(sys.argv[1])
    else:
        # Interactive mode
        main()