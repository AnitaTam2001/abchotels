# quick_export.py
import os
import csv
import psycopg2
from datetime import datetime

def quick_export():
    """Quick export of all data"""
    print("⚡ Quick Export - ABC Hotels Data")
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            dbname='abchotels',
            user='abchotels_user',
            password='abc123hotels',
            host='localhost',
            port='5433'
        )
        
        # Create export directory
        os.makedirs('exports', exist_ok=True)
        
        # Tables to export
        tables = {
            'cities': 'SELECT name, description, is_active FROM hotel_city',
            'room_types': 'SELECT name, description, price_per_night, capacity FROM hotel_roomtype',
            'rooms': '''
                SELECT r.room_number, rt.name, c.name, r.is_available 
                FROM hotel_room r
                JOIN hotel_roomtype rt ON r.room_type_id = rt.id
                JOIN hotel_city c ON r.city_id = c.id
            ''',
            'departments': 'SELECT name, description FROM hotel_department'
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for table_name, query in tables.items():
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
            filename = f"exports/{table_name}_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Get column names from cursor description
                column_names = [desc[0] for desc in cursor.description]
                writer.writerow(column_names)
                
                # Write data
                writer.writerows(data)
            
            print(f"✅ {table_name}: {len(data)} records -> {filename}")
        
        conn.close()
        print(f"\n🎉 Quick export completed! Check 'exports/' directory.")
        
    except Exception as e:
        print(f"❌ Error during export: {e}")

if __name__ == "__main__":
    quick_export()