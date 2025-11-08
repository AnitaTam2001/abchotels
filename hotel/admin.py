# hotel/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import City, RoomType, Room, Booking, FAQ, Department, JobListing, JobApplication

class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'image_preview']  # Added 'id'
    list_filter = ['is_active']
    search_fields = ['name']
    readonly_fields = ['image_preview_large']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.image.url)
        return "No image"
    image_preview_large.short_description = 'Image Preview'

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price_per_night', 'capacity', 'image_preview']  # Added 'id'
    list_filter = ['capacity']
    search_fields = ['name']
    readonly_fields = ['image_preview_large']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.image.url)
        return "No image"
    image_preview_large.short_description = 'Image Preview'

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'city', 'room_type', 'price_per_night', 'capacity', 'is_available', 'image_preview']
    list_filter = ['room_type', 'is_available', 'city']
    search_fields = ['city__name', 'room_type__name']  # Fixed: changed underscore to double underscore for related field lookup
    readonly_fields = ['image_preview_large']

    def price_per_night(self, obj):
        return f"${obj.room_type.price_per_night}"
    price_per_night.short_description = 'Price Per Night'

    def capacity(self, obj):
        return obj.room_type.capacity
    capacity.short_description = 'Capacity'

    def image_preview(self, obj):
        if obj.room_type.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.room_type.image.url)
        return "No image"
    image_preview.short_description = 'Room Image'

    def image_preview_large(self, obj):
        if obj.room_type.image:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.room_type.image.url)
        return "No image"
    image_preview_large.short_description = 'Room Image Preview'

class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'guest_name', 'room', 'check_in', 'check_out', 'status']
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['guest_name', 'guest_email']
    date_hierarchy = 'created_at'

class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'category', 'order', 'is_active']  # Added 'id'
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']  # Added 'id'
    search_fields = ['name']

class JobListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'department', 'job_type', 'experience_level', 'is_active', 'posted_date']  # Added 'id'
    list_filter = ['department', 'job_type', 'experience_level', 'is_active', 'posted_date']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    date_hierarchy = 'posted_date'

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'job', 'status', 'applied_date']  # Added 'id'
    list_filter = ['status', 'job', 'applied_date']
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['applied_date']
    date_hierarchy = 'applied_date'

# Register models
admin.site.register(City, CityAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(JobListing, JobListingAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)