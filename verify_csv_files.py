# verify_csv_files.py
import os
import csv

def verify_csv_files():
    """Verify all CSV files have correct structure"""
    print("🔍 Verifying CSV files...")
    
    files_to_verify = {
        'cities.csv': ['name', 'description', 'is_active'],
        'room_types.csv': ['name', 'description', 'price_per_night', 'capacity'],
        'rooms.csv': ['room_number', 'room_type', 'city', 'is_available'],
        'bookings.csv': ['guest_name', 'guest_email', 'guest_phone', 'room_number', 'check_in', 'check_out', 'total_price', 'status'],
        'departments.csv': ['name', 'description'],
        'job_listings.csv': ['title', 'department', 'job_type', 'experience_level', 'location', 'salary_range', 'description', 'requirements', 'responsibilities', 'benefits', 'is_active', 'application_deadline']
    }
    
    all_valid = True
    
    for filename, expected_headers in files_to_verify.items():
        filepath = f'csv/{filename}'
        
        if not os.path.exists(filepath):
            print(f"❌ {filename}: File not found")
            all_valid = False
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                
                if headers != expected_headers:
                    print(f"❌ {filename}: Invalid headers")
                    print(f"   Expected: {expected_headers}")
                    print(f"   Found: {headers}")
                    all_valid = False
                else:
                    # Count rows
                    file.seek(0)
                    next(reader)  # Skip header
                    row_count = sum(1 for row in reader)
                    print(f"✅ {filename}: Valid ({row_count} rows)")
                    
        except Exception as e:
            print(f"❌ {filename}: Error reading file - {e}")
            all_valid = False
    
    return all_valid

if __name__ == "__main__":
    if verify_csv_files():
        print("\n🎉 All CSV files are valid and ready for import!")
        print("Run: python import_hotel_data.py")
    else:
        print("\n❌ Some CSV files have issues. Please fix them before importing.")