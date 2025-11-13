# import_users.py
import os
import sys
import django
import csv

# Setup Django
sys.path.append('/Users/anita/abchotels')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abchotels.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from hotel.models import CustomUser

def map_permissions(permission_string):
    """Map permission string to Django user fields"""
    permission_map = {
        # Active users
        'active_user': {'is_active': True, 'is_staff': False, 'is_superuser': False},
        'active_staff': {'is_active': True, 'is_staff': True, 'is_superuser': False},
        'active_superuser': {'is_active': True, 'is_staff': True, 'is_superuser': True},
        # Inactive users
        'inactive_user': {'is_active': False, 'is_staff': False, 'is_superuser': False},
        'inactive_staff': {'is_active': False, 'is_staff': True, 'is_superuser': False},
        'inactive_superuser': {'is_active': False, 'is_staff': True, 'is_superuser': True},
    }
    
    return permission_map.get(permission_string.lower(), 
                            {'is_active': True, 'is_staff': False, 'is_superuser': False})

def import_users_from_csv(filename):
    """Import users from CSV file with comprehensive Permissions field"""
    try:
        filepath = os.path.join('csv', filename)
        print(f"Reading from: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            users_created = 0
            users_updated = 0
            
            for row in reader:
                # Map permissions to Django user fields
                permissions = map_permissions(row['Permissions'])
                
                # Check if user already exists
                try:
                    user = CustomUser.objects.get(username=row['Username'])
                    # Update existing user
                    user.email = row['Email']
                    user.phone_number = row['Phone Number']
                    user.first_name = row['First Name']
                    user.last_name = row['Last Name']
                    user.is_active = permissions['is_active']
                    user.is_staff = permissions['is_staff']
                    user.is_superuser = permissions['is_superuser']
                    user.save()
                    users_updated += 1
                    print(f"~ Updated user: {user.username} ({row['Permissions']})")
                    
                except CustomUser.DoesNotExist:
                    # Create new user
                    user = CustomUser.objects.create(
                        username=row['Username'],
                        email=row['Email'],
                        password=make_password(row['Password']),
                        phone_number=row['Phone Number'],
                        first_name=row['First Name'],
                        last_name=row['Last Name'],
                        is_active=permissions['is_active'],
                        is_staff=permissions['is_staff'],
                        is_superuser=permissions['is_superuser'],
                    )
                    users_created += 1
                    print(f"✓ Created user: {user.username} ({row['Permissions']})")
            
            print(f"✓ Import completed: {users_created} created, {users_updated} updated from {filename}")
            return users_created
            
    except FileNotFoundError:
        print(f"✗ File not found: {filename}")
        return 0
    except Exception as e:
        print(f"✗ Error importing users from {filename}: {e}")
        return 0

def check_csv_files():
    """Check if user CSV files exist"""
    print("Checking user CSV files...")
    
    required_files = {
        'import_staff_users.csv': 'Staff Users',
        'import_active_users.csv': 'Active Users'
    }
    
    missing_files = []
    
    for filename, description in required_files.items():
        filepath = os.path.join('csv', filename)
        if os.path.exists(filepath):
            print(f"✓ {description}: {filename}")
        else:
            print(f"✗ {description}: {filename} - FILE NOT FOUND")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n✗ Missing {len(missing_files)} required CSV files:")
        for missing in missing_files:
            print(f" - {missing}")
        return False
    
    print(f"\n✓ All required user CSV files found!")
    return True

def show_current_users():
    """Show current user statistics"""
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    staff_users = CustomUser.objects.filter(is_staff=True).count()
    superusers = CustomUser.objects.filter(is_superuser=True).count()
    regular_users = CustomUser.objects.filter(is_staff=False, is_superuser=False).count()
    
    print(f"\nCURRENT USER STATISTICS:")
    print(f"  Total users: {total_users}")
    print(f"  Active users: {active_users}")
    print(f"  Regular users: {regular_users}")
    print(f"  Staff users: {staff_users}")
    print(f"  Superusers: {superusers}")

def show_permissions_guide():
    """Show permissions mapping guide"""
    print("\n" + "=" * 60)
    print("PERMISSIONS MAPPING GUIDE:")
    print("=" * 60)
    print("active_user       = Active regular user")
    print("active_staff      = Active staff user (admin access)")
    print("active_superuser  = Active admin user (full privileges)")
    print("inactive_user     = Inactive regular user")
    print("inactive_staff    = Inactive staff user")
    print("inactive_superuser= Inactive admin user")
    print("=" * 60)

def import_staff_users_only():
    """Import only staff users"""
    print("\n" + "=" * 40)
    print("IMPORTING STAFF USERS...")
    print("=" * 40)
    
    if not os.path.exists(os.path.join('csv', 'import_staff_users.csv')):
        print("✗ Staff users CSV file not found!")
        return False
    
    count = import_users_from_csv('import_staff_users.csv')
    print("=" * 40)
    print(f"Staff users import completed! {count} users processed")
    return True

def import_regular_users_only():
    """Import only regular users"""
    print("\n" + "=" * 40)
    print("IMPORTING REGULAR USERS...")
    print("=" * 40)
    
    if not os.path.exists(os.path.join('csv', 'import_active_users.csv')):
        print("✗ Regular users CSV file not found!")
        return False
    
    count = import_users_from_csv('import_active_users.csv')
    print("=" * 40)
    print(f"Regular users import completed! {count} users processed")
    return True

def import_all_users():
    """Import all users"""
    print("\n" + "=" * 50)
    print("IMPORTING ALL USERS...")
    print("=" * 50)
    
    # Check if CSV files exist
    if not check_csv_files():
        print("\n✗ Cannot import users - missing CSV files!")
        return False
    
    # Show current state
    show_current_users()
    
    print("\n" + "=" * 50)
    print("STARTING USER IMPORT...")
    print("=" * 50)
    
    # Import staff users
    print("\n1. Importing Staff Users...")
    staff_count = import_users_from_csv('import_staff_users.csv')
    
    # Import regular users
    print("\n2. Importing Regular Users...")
    regular_count = import_users_from_csv('import_active_users.csv')
    
    # Final summary
    print("\n" + "=" * 50)
    print("IMPORT COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    
    show_current_users()
    print(f"\nIMPORT SUMMARY:")
    print(f"  Staff users processed: {staff_count}")
    print(f"  Regular users processed: {regular_count}")
    print(f"  Total users processed: {staff_count + regular_count}")
    
    return True

def clean_all_users():
    """Delete all users except superusers"""
    print("\n" + "=" * 50)
    confirm = input("⚠️  Type 'DELETE' to confirm deleting all non-superuser users: ")
    if confirm.upper() != 'DELETE':
        print("✗ Operation cancelled.")
        return False
    
    # Keep superusers (admins)
    users_to_delete = CustomUser.objects.filter(is_superuser=False)
    count = users_to_delete.count()
    users_to_delete.delete()
    
    print(f"✓ Deleted {count} non-superuser users")
    show_current_users()
    return True

def clean_regular_users_only():
    """Delete only regular users"""
    print("\n" + "=" * 40)
    confirm = input("⚠️  Type 'DELETE' to confirm deleting all regular users: ")
    if confirm.upper() != 'DELETE':
        print("✗ Operation cancelled.")
        return False
    
    # Delete only regular users (non-staff, non-superuser)
    users_to_delete = CustomUser.objects.filter(is_staff=False, is_superuser=False)
    count = users_to_delete.count()
    users_to_delete.delete()
    
    print(f"✓ Deleted {count} regular users")
    show_current_users()
    return True

def clean_staff_users_only():
    """Delete only staff users (non-superuser)"""
    print("\n" + "=" * 40)
    confirm = input("⚠️  Type 'DELETE' to confirm deleting all staff users: ")
    if confirm.upper() != 'DELETE':
        print("✗ Operation cancelled.")
        return False
    
    # Delete only staff users (not superusers)
    users_to_delete = CustomUser.objects.filter(is_staff=True, is_superuser=False)
    count = users_to_delete.count()
    users_to_delete.delete()
    
    print(f"✓ Deleted {count} staff users")
    show_current_users()
    return True

def main_menu():
    """Main interactive menu"""
    while True:
        print("\n" + "=" * 50)
        print("ABC HOTELS - USER MANAGEMENT SYSTEM")
        print("=" * 50)
        
        show_current_users()
        show_permissions_guide()
        
        print("\n" + "=" * 50)
        print("OPTIONS:")
        print("1. IMPORT ALL USERS")
        print("2. IMPORT STAFF USERS ONLY")
        print("3. IMPORT REGULAR USERS ONLY")
        print("4. CLEAN ALL USERS (except superusers)")
        print("5. CLEAN REGULAR USERS ONLY")
        print("6. CLEAN STAFF USERS ONLY")
        print("7. CHECK CSV FILES")
        print("0. EXIT")
        print("=" * 50)
        
        choice = input("\nSelect option (0-7): ").strip()
        
        if choice == '1':
            import_all_users()
        elif choice == '2':
            import_staff_users_only()
        elif choice == '3':
            import_regular_users_only()
        elif choice == '4':
            clean_all_users()
        elif choice == '5':
            clean_regular_users_only()
        elif choice == '6':
            clean_staff_users_only()
        elif choice == '7':
            check_csv_files()
        elif choice == '0':
            print("\nThank you for using ABC Hotels User Management System! 👋")
            break
        else:
            print("✗ Invalid choice! Please select 0-7.")
        
        if choice != '0':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()