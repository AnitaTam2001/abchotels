# hotel/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django import forms
from .models import CustomUser, City, Department, RoomType, Room, Booking, FAQ, JobListing, JobApplication

# Custom User Admin with app_label override
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']

# Unregister the default User model if it's registered
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

# Register CustomUser with explicit app_label
admin.site.register(CustomUser, CustomUserAdmin)


# Rest of your admin classes remain the same...
class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'style': 'width: 80%; font-size: 14px;'})
        self.fields['description'].widget.attrs.update({'rows': 3})

class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
    list_display = ['id', 'name', 'is_active', 'image_preview']
    list_display_links = ['id', 'name']
    list_filter = ['is_active']
    search_fields = ['name']
    readonly_fields = ['image_preview_large']
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 8px;" />', obj.image.url)
        return "No image"
    image_preview_large.short_description = 'Image Preview'

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']
    list_per_page = 20

class RoomTypeAdminForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'style': 'width: 80%; font-size: 14px;'})
        self.fields['description'].widget.attrs.update({'rows': 3})
        self.fields['price_per_night'].widget.attrs.update({'style': 'width: 150px;'})

class RoomTypeAdmin(admin.ModelAdmin):
    form = RoomTypeAdminForm
    list_display = ['id', 'name', 'price_per_night', 'capacity', 'image_preview']
    list_display_links = ['id', 'name']
    list_filter = ['capacity']
    search_fields = ['name']
    readonly_fields = ['image_preview_large']
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 8px;" />', obj.image.url)
        return "No image"
    image_preview_large.short_description = 'Image Preview'

class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].widget.attrs.update({'style': 'width: 300px;'})
        self.fields['room_type'].widget.attrs.update({'style': 'width: 300px;'})

class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    list_display = ['id', 'city', 'room_type', 'price_per_night', 'capacity', 'is_available', 'room_image_preview', 'room_specific_image_preview']
    list_display_links = ['id', 'city']
    list_filter = ['room_type', 'is_available', 'city']
    search_fields = ['city__name', 'room_type__name']
    readonly_fields = ['room_image_preview_large', 'room_specific_image_preview_large']
    list_per_page = 20
    list_select_related = ['city', 'room_type']

    def price_per_night(self, obj):
        return f"${obj.room_type.price_per_night}"
    price_per_night.short_description = 'Price/Night'

    def capacity(self, obj):
        return obj.room_type.capacity
    capacity.short_description = 'Capacity'
    capacity.admin_order_field = 'room_type__capacity'

    def room_image_preview(self, obj):
        if obj.room_type.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', obj.room_type.image.url)
        return "No image"
    room_image_preview.short_description = 'Room Type Image'

    def room_image_preview_large(self, obj):
        if obj.room_type.image:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 8px;" />', obj.room_type.image.url)
        return "No image"
    room_image_preview_large.short_description = 'Room Type Image Preview'

    def room_specific_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', obj.image.url)
        return "No specific image"
    room_specific_image_preview.short_description = 'Room Specific Image'

    def room_specific_image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 8px;" />', obj.image.url)
        return "No specific image"
    room_specific_image_preview_large.short_description = 'Room Specific Image Preview'

class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'guest_name', 'room_display', 'check_in', 'check_out', 'status', 'total_price_display', 'created_at']
    list_filter = ['status', 'check_in', 'check_out', 'created_at']
    search_fields = ['guest_name', 'guest_email', 'room__city__name', 'room__room_type__name']
    readonly_fields = ['created_at', 'updated_at', 'total_price_display']
    list_per_page = 20
    date_hierarchy = 'created_at'

    def room_display(self, obj):
        return str(obj.room)
    room_display.short_description = 'Room'
    room_display.admin_order_field = 'room'

    def total_price_display(self, obj):
        return f"${obj.total_price}"
    total_price_display.short_description = 'Total Price'

class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    list_per_page = 20

class JobListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'department', 'job_type', 'experience_level', 'is_active', 'posted_date']
    list_filter = ['department', 'job_type', 'experience_level', 'is_active', 'posted_date']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    date_hierarchy = 'posted_date'
    list_per_page = 20
    list_select_related = ['department']

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'job_display', 'status', 'applied_date']
    list_filter = ['status', 'job', 'applied_date']
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['applied_date']
    date_hierarchy = 'applied_date'
    list_per_page = 20
    list_select_related = ['job']

    def job_display(self, obj):
        return str(obj.job)
    job_display.short_description = 'Job'

# Register all other models
admin.site.register(City, CityAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(JobListing, JobListingAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)