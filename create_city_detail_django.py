# create_city_detail_django.py
# Run this script to generate the Django-compatible city_detail.html template

def create_city_detail_template():
    """Create the complete city_detail.html template for Django with local images"""
    
    template_content = """<!-- templates/city_detail.html -->
{% extends 'base.html' %}
{% load static %}

{% block content %}
<section style="padding: 2rem 0;">
  <div class="container">
    <!-- City Header with Photo -->
    <div style="position: relative; margin-bottom: 3rem;">
      <div style="height: 400px; overflow: hidden; border-radius: 15px;">
        {% if city.name == 'New York' %}
        <img src="{% static 'images/cities/new_york.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'London' %}
        <img src="{% static 'images/cities/london.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Paris' %}
        <img src="{% static 'images/cities/paris.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Tokyo' %}
        <img src="{% static 'images/cities/tokyo.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Dubai' %}
        <img src="{% static 'images/cities/dubai.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Singapore' %}
        <img src="{% static 'images/cities/singapore.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Bangkok' %}
        <img src="{% static 'images/cities/bangkok.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Sydney' %}
        <img src="{% static 'images/cities/sydney.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Rome' %}
        <img src="{% static 'images/cities/rome.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Barcelona' %}
        <img src="{% static 'images/cities/barcelona.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Istanbul' %}
        <img src="{% static 'images/cities/istanbul.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Hong Kong' %}
        <img src="{% static 'images/cities/hong_kong.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Los Angeles' %}
        <img src="{% static 'images/cities/los_angeles.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Miami' %}
        <img src="{% static 'images/cities/miami.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Las Vegas' %}
        <img src="{% static 'images/cities/las_vegas.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Chicago' %}
        <img src="{% static 'images/cities/chicago.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'San Francisco' %}
        <img src="{% static 'images/cities/san_francisco.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Amsterdam' %}
        <img src="{% static 'images/cities/amsterdam.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Vienna' %}
        <img src="{% static 'images/cities/vienna.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% elif city.name == 'Prague' %}
        <img src="{% static 'images/cities/prague.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% else %}
        <img src="{% static 'images/cities/default.jpg' %}" alt="{{ city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% endif %}
      </div>
      <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.7)); padding: 2rem; color: white;">
        <h1 style="margin: 0; font-size: 3rem; font-weight: bold;">{{ city.name }}</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">{{ city.description }}</p>
      </div>
    </div>

    <!-- Available Rooms Section -->
    <div style="margin-bottom: 3rem;">
      <h2 style="margin-bottom: 2rem; color: #2c3e50;">Available Room Types in {{ city.name }}</h2>
      {% if room_types %}
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem;">
        {% for room_type in room_types %}
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #f0f0f0;">
          <div style="height: 200px; overflow: hidden;">
            {% if room_type.name == 'Standard King' %}
            <img src="{% static 'images/rooms/standard_king.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif room_type.name == 'Standard Twin' %}
            <img src="{% static 'images/rooms/standard_twin.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif room_type.name == 'Deluxe King' %}
            <img src="{% static 'images/rooms/deluxe_king.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif room_type.name == 'Deluxe Suite' %}
            <img src="{% static 'images/rooms/deluxe_suite.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif room_type.name == 'Executive King' %}
            <img src="{% static 'images/rooms/executive_king.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif room_type.name == 'Executive Suite' %}
            <img src="{% static 'images/rooms/executive_suite.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif room_type.name == 'Presidential Suite' %}
            <img src="{% static 'images/rooms/presidential_suite.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif room_type.name == 'Family Suite' %}
            <img src="{% static 'images/rooms/family_suite.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif room_type.name == 'Honeymoon Suite' %}
            <img src="{% static 'images/rooms/honeymoon_suite.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% else %}
            <img src="{% static 'images/rooms/standard_king.png' %}" alt="{{ room_type.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% endif %}
          </div>
          <div style="padding: 1.5rem;">
            <h3 style="margin: 0 0 1rem 0; color: #2c3e50;">{{ room_type.name }}</h3>
            <p style="color: #666; margin-bottom: 1rem; line-height: 1.6;">{{ room_type.description }}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
              <div>
                <strong style="color: #e74c3c; font-size: 1.3rem;">${{ room_type.price_per_night }}</strong>
                <span style="color: #666;">/ night</span>
              </div>
              <div style="color: #666;">
                <strong>Capacity:</strong> {{ room_type.capacity }} person{{ room_type.capacity|pluralize }}
              </div>
            </div>
            <a href="{% url 'room_type_detail' room_type.id %}" class="btn" style="width: 100%; text-align: center; background: #3498db; color: white; padding: 12px; border-radius: 6px; text-decoration: none; display: block;">
              View Available Rooms
            </a>
          </div>
        </div>
        {% endfor %}
      </div>
      {% else %}
      <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 8px;">
        <p style="color: #666; margin: 0;">No rooms available in {{ city.name }} at the moment.</p>
      </div>
      {% endif %}
    </div>

    <!-- Other Cities Section -->
    {% if other_cities %}
    <div style="border-top: 2px solid #f0f0f0; padding-top: 3rem;">
      <h2 style="margin-bottom: 2rem; color: #2c3e50;">Explore Other Destinations</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
        {% for other_city in other_cities %}
        <div style="background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #f0f0f0;">
          <div style="height: 150px; overflow: hidden;">
            {% if other_city.name == 'New York' %}
            <img src="{% static 'images/cities/new_york.jpg' %}" alt="{{ other_city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif other_city.name == 'London' %}
            <img src="{% static 'images/cities/london.jpg' %}" alt="{{ other_city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif other_city.name == 'Paris' %}
            <img src="{% static 'images/cities/paris.jpg' %}" alt="{{ other_city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif other_city.name == 'Tokyo' %}
            <img src="{% static 'images/cities/tokyo.jpg' %}" alt="{{ other_city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif other_city.name == 'Dubai' %}
            <img src="{% static 'images/cities/dubai.jpg' %}" alt="{{ other_city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% elif other_city.name == 'Singapore' %}
            <img src="{% static 'images/cities/singapore.jpg' %}" alt="{{ other_city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% else %}
            <img src="{% static 'images/cities/default.jpg' %}" alt="{{ other_city.name }}" style="width: 100%; height: 100%; object-fit: cover;">
            {% endif %}
          </div>
          <div style="padding: 1rem;">
            <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">{{ other_city.name }}</h4>
            <p style="color: #666; font-size: 0.9rem; margin: 0 0 1rem 0; line-height: 1.4;">{{ other_city.description|truncatewords:10 }}</p>
            <a href="{% url 'city_detail' other_city.id %}" style="color: #3498db; text-decoration: none; font-weight: 500;">Explore →</a>
          </div>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}
  </div>
</section>

<style>
.btn {
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #2980b9 !important;
}
</style>
{% endblock %}
"""

    # Create the templates directory if it doesn't exist
    import os
    os.makedirs('templates', exist_ok=True)
    
    # Write the template file
    with open('templates/city_detail.html', 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print("✅ SUCCESS: Django-compatible templates/city_detail.html has been created!")
    return True

def show_instructions():
    """Show instructions for required images"""
    print("\n📋 REQUIRED IMAGE FILES (with underscores):")
    print("\n🏙️  City Images (save in static/images/cities/):")
    cities = [
        'new_york.jpg', 'london.jpg', 'paris.jpg', 'tokyo.jpg', 'dubai.jpg',
        'singapore.jpg', 'bangkok.jpg', 'sydney.jpg', 'rome.jpg', 'barcelona.jpg',
        'istanbul.jpg', 'hong_kong.jpg', 'los_angeles.jpg', 'miami.jpg', 'las_vegas.jpg',
        'chicago.jpg', 'san_francisco.jpg', 'amsterdam.jpg', 'vienna.jpg', 'prague.jpg',
        'default.jpg'
    ]
    for city in cities:
        print(f"   📷 {city}")
    
    print("\n🛏️  Room Type Images (save in static/images/rooms/):")
    rooms = [
        'standard_king.png', 'standard_twin.png', 'deluxe_king.png', 
        'deluxe_suite.png', 'executive_king.png', 'executive_suite.png',
        'presidential_suite.png', 'family_suite.png', 'honeymoon_suite.png'
    ]
    for room in rooms:
        print(f"   🛏️  {room}")
    
    print("\n🔧 KEY CHANGES FOR DJANGO:")
    print("   ✅ Uses {% load static %} at the top")
    print("   ✅ Uses {% static 'path/to/image.jpg' %} instead of url_for()")
    print("   ✅ Uses {% url 'view_name' arg %} for URL routing")
    print("   ✅ File names use underscores (new_york.jpg instead of newyork.jpg)")

if __name__ == "__main__":
    print("🏨 Creating Django-compatible city_detail.html template...")
    print("=" * 60)
    
    if create_city_detail_template():
        show_instructions()
        print("\n🚀 NEXT STEPS:")
        print("1. Add your city images to static/images/cities/")
        print("2. Add your room images to static/images/rooms/")
        print("3. Make sure your Django settings.py has STATIC_URL configured")
        print("4. Run your Django server: python manage.py runserver")
        print("5. Visit: http://localhost:8000/city/391/")
    else:
        print("❌ Failed to create template")