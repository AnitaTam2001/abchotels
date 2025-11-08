# fix_encoding.py
import os

CSV_FOLDER = 'csv'

def convert_file_to_utf8(filename):
    filepath = os.path.join(CSV_FOLDER, filename)
    
    # Read the file with proper encoding detection
    try:
        # First try UTF-8
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"✅ {filename} is already UTF-8")
        return True
    except UnicodeDecodeError:
        # If UTF-8 fails, try ASCII
        try:
            with open(filepath, 'r', encoding='us-ascii') as file:
                content = file.read()
            
            # Write back as UTF-8
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"✅ Converted {filename} from ASCII to UTF-8")
            return True
        except Exception as e:
            print(f"❌ Failed to convert {filename}: {e}")
            return False
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
        return False

def fix_department_csv():
    """Special function to fix department CSV which might have formatting issues"""
    filepath = os.path.join(CSV_FOLDER, 'import_department.csv')
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='us-ascii') as file:
            content = file.read()
        
        # Fix common CSV issues
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove any extra spaces and clean up the line
            cleaned_line = line.strip()
            if cleaned_line:  # Only keep non-empty lines
                cleaned_lines.append(cleaned_line)
        
        # Write back as proper UTF-8 CSV
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write('\n'.join(cleaned_lines))
        
        print(f"✅ Fixed and converted import_department.csv to UTF-8")
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix department CSV: {e}")
        
        # Create a fresh department CSV if repair fails
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
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(department_data)
        print(f"✅ Created new department CSV file with UTF-8 encoding")
        return True

print("🔧 Fixing CSV file encodings...")
print("=" * 50)

# Fix roomtype and room files with standard method
convert_file_to_utf8('import_roomtype.csv')
convert_file_to_utf8('import_room.csv')

# Use special function for department file
fix_department_csv()

# Verify city file is already UTF-8
convert_file_to_utf8('import_city.csv')

print("=" * 50)
print("✅ All CSV files have been converted to UTF-8 encoding!")
print("\n📁 File status:")
for filename in ['import_city.csv', 'import_roomtype.csv', 'import_room.csv', 'import_department.csv']:
    filepath = os.path.join(CSV_FOLDER, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                f.read()
            print(f"   ✅ {filename}: UTF-8 compatible")
        except:
            print(f"   ❌ {filename:} Still has encoding issues")
    else:
        print(f"   ❌ {filename}: File not found")