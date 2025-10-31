# hotel/admin.py
from django.contrib import admin
from .models import City, RoomType, Room, Booking, FAQ, Department, JobListing, JobApplication
# hotel/admin.py

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_night', 'capacity']
    list_filter = ['capacity']
    search_fields = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'is_available']
    list_filter = ['room_type', 'is_available']
    search_fields = ['room_number']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'guest_name', 'room', 'check_in', 'check_out', 'status']
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['guest_name', 'guest_email']
    date_hierarchy = 'created_at'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['question', 'answer']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'job_type', 'experience_level', 'is_active', 'posted_date']
    list_filter = ['department', 'job_type', 'experience_level', 'is_active', 'posted_date']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    date_hierarchy = 'posted_date'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'job', 'status', 'applied_date']
    list_filter = ['status', 'job', 'applied_date']
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['applied_date']
    date_hierarchy = 'applied_date'