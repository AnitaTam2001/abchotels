# import_hotel_data_fixed.py
import os
import csv
from datetime import datetime
import psycopg2

def get_db_connection():
    """Create direct PostgreSQL connection"""
    try:
        conn = psycopg2.connect(
            dbname='abchotels',
            user='abchotels_user',
            password='abc123hotels',
            host='localhost',
            port='5433'
        )
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

def clear_existing_data(conn):
    """Clear all existing data from tables"""
    print("🗑️  Clearing existing data...")
    try:
        cursor = conn.cursor()
        # Clear in reverse order to respect foreign key constraints
        tables = [
            'hotel_joblisting',
            'hotel_jobapplication',
            'hotel_booking', 
            'hotel_room',
            'hotel_roomtype',
            'hotel_city',
            'hotel_department',
            'hotel_faq'
        ]
        
        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"   ✅ Cleared {table}")
        
        # Reset sequences
        cursor.execute("""
            SELECT sequence_name 
            FROM information_schema.sequences 
            WHERE sequence_schema = 'public'
        """)
        sequences = [row[0] for row in cursor.fetchall()]
        
        for sequence in sequences:
            cursor.execute(f"ALTER SEQUENCE {sequence} RESTART WITH 1")
        
        conn.commit()
        print("✅ All existing data cleared and sequences reset!")
        return True
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        conn.rollback()
        return False

def check_csv_format():
    """Check and fix CSV format issues"""
    print("🔍 Checking CSV formats...")
    
    # Fix room_types.csv - remove quotes from capacity values
    try:
        with open('csv/room_types.csv', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix common CSV format issues
        content = content.replace('", "', '","')  # Remove spaces between quotes
        content = content.replace('"', '')  # Remove all quotes
        
        with open('csv/room_types_fixed.csv', 'w', encoding='utf-8') as file:
            file.write(content)
        print("✅ Fixed room_types.csv format")
    except Exception as e:
        print(f"❌ Error fixing room_types.csv: {e}")

def import_cities(conn):
    """Import cities from CSV"""
    print("📊 Importing cities...")
    try:
        cursor = conn.cursor()
        with open('csv/cities.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                cursor.execute(
                    "INSERT INTO hotel_city (name, description, is_active) VALUES (%s, %s, %s)",
                    (row['name'], row['description'], row.get('is_active', 'True').lower() == 'true')
                )
                count += 1
        conn.commit()
        print(f"✅ Cities imported successfully! Added {count} new cities.")
    except FileNotFoundError:
        print("❌ cities.csv not found")
    except Exception as e:
        print(f"❌ Error importing cities: {e}")
        conn.rollback()

def import_room_types(conn):
    """Import room types from CSV"""
    print("📊 Importing room types...")
    try:
        cursor = conn.cursor()
        # Try the fixed file first, then fall back to original
        csv_file = 'csv/room_types_fixed.csv' if os.path.exists('csv/room_types_fixed.csv') else 'csv/room_types.csv'
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                try:
                    # Clean the data
                    price = float(str(row['price_per_night']).replace('"', '').strip())
                    capacity = int(str(row['capacity']).replace('"', '').strip())
                    
                    cursor.execute(
                        "INSERT INTO hotel_roomtype (name, description, price_per_night, capacity) VALUES (%s, %s, %s, %s)",
                        (row['name'], row['description'], price, capacity)
                    )
                    count += 1
                except ValueError as e:
                    print(f"❌ Skipping room type {row['name']}: Invalid number format - {e}")
                    
        conn.commit()
        print(f"✅ Room types imported successfully! Added {count} new room types.")
    except FileNotFoundError:
        print("❌ room_types.csv not found")
    except Exception as e:
        print(f"❌ Error importing room types: {e}")
        conn.rollback()

def import_departments(conn):
    """Import departments from CSV"""
    print("📊 Importing departments...")
    try:
        cursor = conn.cursor()
        with open('csv/departments.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                cursor.execute(
                    "INSERT INTO hotel_department (name, description) VALUES (%s, %s)",
                    (row['name'], row.get('description', ''))
                )
                count += 1
        conn.commit()
        print(f"✅ Departments imported successfully! Added {count} new departments.")
    except FileNotFoundError:
        print("❌ departments.csv not found")
    except Exception as e:
        print(f"❌ Error importing departments: {e}")
        conn.rollback()

def import_job_listings(conn):
    """Import job listings from CSV - fixed version"""
    print("📊 Importing job listings...")
    try:
        cursor = conn.cursor()
        with open('csv/job_listings.csv', 'r', encoding='utf-8') as file:
            # Read the entire file to inspect structure
            lines = file.readlines()
            
        # Parse manually to handle the complex structure
        if len(lines) > 1:
            headers = [h.strip('"') for h in lines[0].strip().split('","')]
            
            count = 0
            skipped = 0
            
            for line in lines[1:]:
                try:
                    # Split by comma but handle quoted fields
                    values = []
                    in_quotes = False
                    current_value = ""
                    
                    for char in line.strip():
                        if char == '"':
                            in_quotes = not in_quotes
                        elif char == ',' and not in_quotes:
                            values.append(current_value.strip('"'))
                            current_value = ""
                        else:
                            current_value += char
                    
                    if current_value:
                        values.append(current_value.strip('"'))
                    
                    if len(values) >= len(headers):
                        row = dict(zip(headers, values))
                        
                        # Get department ID
                        cursor.execute("SELECT id FROM hotel_department WHERE name = %s", (row['department'],))
                        dept_result = cursor.fetchone()
                        
                        if dept_result:
                            dept_id = dept_result[0]
                            
                            # Handle application deadline safely
                            app_deadline = None
                            deadline_str = row.get('application_deadline', '').strip()
                            if deadline_str and len(deadline_str) == 10 and deadline_str.count('-') == 2:
                                try:
                                    app_deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                                except ValueError:
                                    app_deadline = None
                            
                            cursor.execute(
                                """INSERT INTO hotel_joblisting 
                                (title, department_id, job_type, experience_level, location, salary_range, 
                                 description, requirements, responsibilities, benefits, is_active, 
                                 posted_date, application_deadline) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (
                                    row['title'],
                                    dept_id,
                                    row['job_type'],
                                    row['experience_level'],
                                    row.get('location', 'Main Hotel'),
                                    row.get('salary_range', ''),
                                    row['description'],
                                    row['requirements'],
                                    row['responsibilities'],
                                    row.get('benefits', ''),
                                    row.get('is_active', 'True').lower() == 'true',
                                    datetime.now(),
                                    app_deadline
                                )
                            )
                            count += 1
                        else:
                            print(f"❌ Skipping job listing: Department '{row.get('department', 'Unknown')}' not found")
                            skipped += 1
                    else:
                        skipped += 1
                        
                except Exception as e:
                    print(f"❌ Skipping job listing: {e}")
                    skipped += 1
                    
        conn.commit()
        print(f"✅ Job listings imported successfully! Added {count} new job listings. Skipped {skipped}.")
    except FileNotFoundError:
        print("❌ job_listings.csv not found")
    except Exception as e:
        print(f"❌ Error importing job listings: {e}")
        conn.rollback()

def check_database_tables(conn):
    """Check if database tables exist"""
    print("🔍 Checking database tables...")
    tables = [
        'hotel_city',
        'hotel_roomtype', 
        'hotel_department',
        'hotel_joblisting'
    ]
    
    cursor = conn.cursor()
    missing_tables = []
    
    for table in tables:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            )
        """, (table,))
        exists = cursor.fetchone()[0]
        
        if not exists:
            missing_tables.append(table)
    
    if missing_tables:
        print("❌ Missing database tables:")
        for table in missing_tables:
            print(f"   - {table}")
        return False
    else:
        print("✅ All required database tables exist!")
        return True

def check_csv_files():
    """Check if all required CSV files exist"""
    print("🔍 Checking CSV files...")
    required_files = [
        'csv/cities.csv',
        'csv/room_types.csv',
        'csv/departments.csv',
        'csv/job_listings.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing CSV files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required CSV files found!")
        return True

def main():
    """Main import function"""
    print("🚀 Starting ABC Hotels Data Import (PostgreSQL)...")
    print("=" * 50)
    
    # Ask if user wants to clear existing data
    response = input("\n❓ Do you want to CLEAR ALL EXISTING DATA before importing? (yes/no): ").strip().lower()
    clear_data = response in ['yes', 'y', '1']
    
    # Check if CSV files exist
    if not check_csv_files():
        print("\n❌ Please generate the CSV files first")
        return
    
    # Connect to database
    print("\n🔗 Connecting to PostgreSQL database...")
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        # Check if database tables exist
        if not check_database_tables(conn):
            print("\n❌ Please run Django migrations first:")
            print("   python manage.py makemigrations")
            print("   python manage.py migrate")
            return
        
        # Clear data if requested
        if clear_data:
            if not clear_existing_data(conn):
                print("❌ Data clearing failed. Aborting import.")
                return
        else:
            print("ℹ️  Keeping existing data (may cause duplicates)")
        
        # Fix CSV formats
        check_csv_format()
        
        print("\n📥 Beginning data import...")
        
        # Import in correct order to maintain foreign key relationships
        import_cities(conn)
        import_room_types(conn)
        import_departments(conn)
        import_job_listings(conn)
        
        print("\n" + "=" * 50)
        print("🎉 All data import completed!")
        
        # Display summary
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM hotel_city")
        cities_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM hotel_roomtype")
        room_types_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM hotel_department")
        departments_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM hotel_joblisting")
        job_listings_count = cursor.fetchone()[0]
        
        print("\n📊 Import Summary:")
        print(f"   Cities: {cities_count}")
        print(f"   Room Types: {room_types_count}")
        print(f"   Departments: {departments_count}")
        print(f"   Job Listings: {job_listings_count}")
        
    finally:
        conn.close()
        print("🔒 Database connection closed.")

if __name__ == "__main__":
    main()