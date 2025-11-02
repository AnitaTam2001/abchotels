import os
import requests
import csv
from PIL import Image
import io
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# UNIQUE Unsplash image URLs for each city
CITY_IMAGE_MAPPING = {
    'New York': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'London': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Paris': 'https://images.unsplash.com/photo-1502602898536-47ad22581b52?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Tokyo': 'https://images.unsplash.com/photo-1540959733332-0d2cd6c611b7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Dubai': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Singapore': 'https://images.unsplash.com/photo-1525625293386-3f8f1938fedd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Bangkok': 'https://images.unsplash.com/photo-1558422504-614fb2fc46a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Sydney': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Rome': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Barcelona': 'https://images.unsplash.com/photo-1583422409516-2895a77efded?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Istanbul': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Hong Kong': 'https://images.unsplash.com/photo-1534008897995-27a23e859048?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Los Angeles': 'https://images.unsplash.com/photo-1515896769750-31548aa180f9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Miami': 'https://images.unsplash.com/photo-1514214246283-d427a95c5d2f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Las Vegas': 'https://images.unsplash.com/photo-1605833556294-ea5c7a74f57d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Chicago': 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'San Francisco': 'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Amsterdam': 'https://images.unsplash.com/photo-1459679749680-18eb1eb37418?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Vienna': 'https://images.unsplash.com/photo-1516550893923-42d28e5677af?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Prague': 'https://images.unsplash.com/photo-1592906209472-a36b1f3782ef?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80'
}

# Alternative unique image URLs in case some fail
BACKUP_IMAGE_URLS = {
    'New York': 'https://images.unsplash.com/photo-1485738422979-f5c462d49f74?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'London': 'https://images.unsplash.com/photo-1505761671935-60b3a7427bad?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Paris': 'https://images.unsplash.com/photo-1431274172761-fca41d930114?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Tokyo': 'https://images.unsplash.com/photo-1540959733332-0d2cd6c611b7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Dubai': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Singapore': 'https://images.unsplash.com/photo-1526495124232-a04e1849168c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Bangkok': 'https://images.unsplash.com/photo-1563492065599-3520f775eeed?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Sydney': 'https://images.unsplash.com/photo-1528072164453-f4e8ef0d475a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Rome': 'https://images.unsplash.com/photo-1555992828-ca4dbe41fd4c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Barcelona': 'https://images.unsplash.com/photo-1589329492135-94b3c77b59eb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Istanbul': 'https://images.unsplash.com/photo-1527838832700-5059252407fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Hong Kong': 'https://images.unsplash.com/photo-1531259683007-016a7b628fc3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Los Angeles': 'https://images.unsplash.com/photo-1575917649705-5c03f147b1b9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Miami': 'https://images.unsplash.com/photo-1542259009471-f35b6e17c5a9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Las Vegas': 'https://images.unsplash.com/photo-1605833556294-ea5c7a74f57d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Chicago': 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'San Francisco': 'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Amsterdam': 'https://images.unsplash.com/photo-1534351590666-13e3e96b5017?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Vienna': 'https://images.unsplash.com/photo-1516550893923-42d28e5677af?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    'Prague': 'https://images.unsplash.com/photo-1592906209472-a36b1f3782ef?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80'
}

class CityImageDownloader:
    def __init__(self):
        self.output_dir = 'static/images/cities'
        self.create_directories()
    
    def create_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"Created directory: {self.output_dir}")
    
    def get_city_image_url(self, city_name, use_backup=False):
        """Get image URL for a city"""
        if use_backup:
            return BACKUP_IMAGE_URLS.get(city_name, CITY_IMAGE_MAPPING.get(city_name))
        return CITY_IMAGE_MAPPING.get(city_name)
    
    def download_and_process_image(self, image_url, output_path, max_size=(800, 600)):
        """Download and process image with optimization"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            print(f"Downloading: {image_url}")
            response = requests.get(image_url, timeout=20, headers=headers)
            response.raise_for_status()
            
            # Check if we got actual image data
            if len(response.content) < 5000:  # Too small, probably not an image
                print(f"⚠️  Image too small ({len(response.content)} bytes), might be invalid")
                return False
            
            # Open image with PIL
            image = Image.open(io.BytesIO(response.content))
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            
            # Resize if larger than max_size while maintaining aspect ratio
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save as optimized JPG
            image.save(output_path, 'JPEG', quality=85, optimize=True)
            
            file_size = os.path.getsize(output_path)
            print(f"✓ Saved: {output_path} ({file_size} bytes)")
            return True
            
        except Exception as e:
            print(f"✗ Failed to download {image_url}: {e}")
            return False
    
    def download_city_image(self, city_name):
        """Download image for a single city with backup URLs"""
        filename = f"{city_name.lower().replace(' ', '_')}.jpg"
        output_path = os.path.join(self.output_dir, filename)
        
        # Skip if file already exists and is valid
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 5000:  # Check if file is valid
                print(f"✓ Already exists: {filename} ({file_size} bytes)")
                return True
            else:
                print(f"⚠️  Existing file too small, re-downloading: {filename}")
                os.remove(output_path)
        
        # Try primary URL first
        image_url = self.get_city_image_url(city_name)
        if image_url and self.download_and_process_image(image_url, output_path):
            return True
        
        # Try backup URL if primary fails
        print(f"Trying backup URL for {city_name}...")
        backup_url = self.get_city_image_url(city_name, use_backup=True)
        if backup_url and backup_url != image_url:
            return self.download_and_process_image(backup_url, output_path)
        
        print(f"✗ All URLs failed for {city_name}")
        return False
    
    def download_all_cities_from_csv(self, csv_path='csv/cities.csv'):
        """Download images for all cities in CSV file"""
        print("Starting city image download with UNIQUE images...")
        print("=" * 60)
        
        if not os.path.exists(csv_path):
            print(f"✗ CSV file not found: {csv_path}")
            print("Creating sample CSV file...")
            self.create_sample_csv(csv_path)
        
        success_count = 0
        total_count = 0
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            cities = list(reader)
            total_count = len(cities)
            
            for row in cities:
                city_name = row['name'].strip()
                is_active = row.get('is_active', 'True').strip().lower() == 'true'
                
                if not is_active:
                    print(f"⏭ Skipping inactive city: {city_name}")
                    continue
                
                print(f"\n📍 Processing: {city_name}")
                if self.download_city_image(city_name):
                    success_count += 1
                else:
                    print(f"✗ Failed to download image for {city_name}")
        
        print(f"\n{'='*60}")
        print("DOWNLOAD SUMMARY")
        print(f"{'='*60}")
        print(f"Total cities processed: {total_count}")
        print(f"Successfully downloaded: {success_count}")
        print(f"Failed: {total_count - success_count}")
        print(f"Images saved to: {self.output_dir}")
        
        return success_count
    
    def create_sample_csv(self, csv_path):
        """Create a sample CSV file if it doesn't exist"""
        sample_data = """name,description,is_active
New York,The vibrant city that never sleeps with iconic landmarks like Times Square and Central Park,True
London,Historic city with royal heritage,True
Paris,The romantic city of love with famous museums,True
Tokyo,Modern metropolis blending ancient tradition with cutting-edge technology,True
Dubai,Luxurious desert city with stunning architecture and world-class shopping,True
Singapore,Green city-state known for its efficiency and Gardens by the Bay,True
Bangkok,Vibrant city with ornate temples,True
Sydney,Coastal city famous for its Opera House and beautiful harbor,True
Rome,Eternal city with ancient history,True
Barcelona,Cosmopolitan city with Gaudi architecture and Mediterranean beaches,True
Istanbul,City straddling two continents with rich history and stunning mosques,True
Hong Kong,Dynamic financial hub with stunning skyline and mountain hikes,True
Los Angeles,Entertainment capital with beaches,True
Miami,Tropical paradise with art deco architecture and vibrant nightlife,True
Las Vegas,Entertainment capital with world-class casinos and spectacular shows,True
Chicago,Windy City known for architecture,True
San Francisco,Hilly city with Golden Gate Bridge,True
Amsterdam,Canal-lined city with artistic heritage,True
Vienna,Imperial capital known for classical music and coffee house culture,True
Prague,City of a hundred spires with medieval architecture and charming streets,True"""
        
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(sample_data)
        print(f"Created sample CSV file: {csv_path}")
    
    def list_downloaded_images(self):
        """List all downloaded city images with preview"""
        print(f"\n📁 Downloaded city images in {self.output_dir}:")
        print("-" * 50)
        
        if not os.path.exists(self.output_dir):
            print("No images directory found")
            return
        
        images = [f for f in os.listdir(self.output_dir) if f.endswith('.jpg')]
        for image in sorted(images):
            file_path = os.path.join(self.output_dir, image)
            file_size = os.path.getsize(file_path)
            city_name = image.replace('.jpg', '').replace('_', ' ').title()
            print(f"🏙️  {city_name:15} → {image:20} ({file_size:6} bytes)")

def main():
    """Main function to run the downloader"""
    downloader = CityImageDownloader()
    
    # Download images from CSV
    success_count = downloader.download_all_cities_from_csv()
    
    # List downloaded images
    downloader.list_downloaded_images()
    
    if success_count > 0:
        print(f"\n🎉 Successfully downloaded {success_count} UNIQUE city images!")
        print(f"📍 Location: {downloader.output_dir}")
        print("\nEach city has a different, high-quality photo!")
    else:
        print("\n❌ No images were downloaded. Please check the CSV file path.")

if __name__ == "__main__":
    main()