# import_users.py
import os
import sys
import django
import csv
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abchotels.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction

def import_users_from_csv(csv_file_path):
    """
    Import users from CSV file into Django's default User model
    CSV format should be: username,email,password,first_name,last_name,phone_number
    """
    
    users_created = 0
    users_updated = 0
    errors = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            with transaction.atomic():
                for row_num, row in enumerate(reader, start=2):  # start=2 to account for header
                    try:
                        username = row.get('username', '').strip()
                        email = row.get('email', '').strip()
                        password = row.get('password', '').strip()
                        first_name = row.get('first_name', '').strip()
                        last_name = row.get('last_name', '').strip()
                        phone_number = row.get('phone_number', '').strip()
                        
                        # Validate required fields
                        if not username:
                            errors.append(f"Row {row_num}: Missing username")
                            continue
                            
                        if not email:
                            errors.append(f"Row {row_num}: Missing email")
                            continue
                            
                        if not password:
                            errors.append(f"Row {row_num}: Missing password")
                            continue
                        
                        # Check if user already exists
                        user, created = User.objects.get_or_create(
                            username=username,
                            defaults={
                                'email': email,
                                'first_name': first_name,
                                'last_name': last_name,
                                'is_active': True,
                                'date_joined': datetime.now()
                            }
                        )
                        
                        if created:
                            # Set password for new user
                            user.set_password(password)
                            user.save()
                            users_created += 1
                            print(f"✓ Created user: {username}")
                        else:
                            # Update existing user
                            user.email = email
                            user.first_name = first_name
                            user.last_name = last_name
                            user.save()
                            users_updated += 1
                            print(f"↻ Updated user: {username}")
                            
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                        print(f"✗ Error in row {row_num}: {str(e)}")
        
        # Print summary
        print(f"\n=== Import Summary ===")
        print(f"Users created: {users_created}")
        print(f"Users updated: {users_updated}")
        print(f"Total errors: {len(errors)}")
        
        if errors:
            print(f"\n=== Errors ===")
            for error in errors:
                print(error)
                
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")

def create_sample_csv():
    """Create a sample CSV file for testing"""
    sample_data = [
        ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number'],
        ['john_doe', 'john@example.com', 'password123', 'John', 'Doe', '+1234567890'],
        ['jane_smith', 'jane@example.com', 'password123', 'Jane', 'Smith', '+1234567891'],
        ['bob_wilson', 'bob@example.com', 'password123', 'Bob', 'Wilson', '+1234567892'],
        ['alice_brown', 'alice@example.com', 'password123', 'Alice', 'Brown', '+1234567893'],
        ['charlie_davis', 'charlie@example.com', 'password123', 'Charlie', 'Davis', '+1234567894']
    ]
    
    with open('sample_users.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sample_data)
    
    print("Sample CSV created: sample_users.csv")

if __name__ == "__main__":
    # Check if CSV file path is provided as argument
    if len(sys.argv) > 1:
        csv_file_path = sys.argv[1]
    else:
        # Use default CSV file
        csv_file_path = 'users.csv'
    
    # Check if file exists, if not create sample
    if not os.path.exists(csv_file_path):
        print(f"CSV file '{csv_file_path}' not found.")
        create_sample = input("Would you like to create a sample CSV file? (y/n): ")
        if create_sample.lower() == 'y':
            create_sample_csv()
            print("\nSample CSV created. Please edit 'sample_users.csv' with your user data and run the script again.")
        else:
            print("Please provide a valid CSV file path.")
        sys.exit(1)
    
    print(f"Importing users from: {csv_file_path}")
    confirm = input("Continue? (y/n): ")
    
    if confirm.lower() == 'y':
        import_users_from_csv(csv_file_path)
    else:
        print("Import cancelled.")