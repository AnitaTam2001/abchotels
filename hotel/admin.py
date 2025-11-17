# hotel/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django import forms
from .models import City, Department, RoomType, Room, Booking, FAQ, JobListing, JobApplication, UserProfile

# ================================
# USER PROFILE INLINE ADMIN
# ================================

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['phone_number']
    extra = 1

# ================================
# CUSTOM USER ADMIN
# ================================

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_phone_number', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'groups']
    
    def get_phone_number(self, obj):
        if hasattr(obj, 'profile') and obj.profile.phone_number:
            return obj.profile.phone_number
        return "No phone"
    get_phone_number.short_description = 'Phone Number'

# ================================
# USER PROFILE ADMIN (Standalone)
# ================================

class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make user field 2 times the default width
        self.fields['user'].widget.attrs.update({
            'style': 'width: 600px;',  # 2 times the default user field width
        })
        # Keep phone_number at normal width
        self.fields['phone_number'].widget.attrs.update({
            'style': 'width: 300px;',
        })

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm
    list_display = ['user', 'phone_number', 'user_email', 'user_first_name',
                   'user_last_name', 'user_is_staff', 'user_is_active']
    list_filter = ['user__is_staff', 'user__is_active']
    search_fields = ['user__username', 'user__email', 'phone_number',
                    'user__first_name', 'user__last_name']
    readonly_fields = ['user_info', 'user_permissions_display',
                      'user_important_dates']
    list_per_page = 25
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'user_info')
        }),
        ('Permissions', {
            'fields': ('user_permissions_display',),
            'classes': ('collapse',),
        }),
        ('Important dates', {
            'fields': ('user_important_dates',),
            'classes': ('collapse',),
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'
    user_first_name.admin_order_field = 'user__first_name'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'
    user_last_name.admin_order_field = 'user__last_name'

    def user_is_staff(self, obj):
        return obj.user.is_staff
    user_is_staff.short_description = 'Staff'
    user_is_staff.boolean = True
    user_is_staff.admin_order_field = 'user__is_staff'

    def user_is_active(self, obj):
        return obj.user.is_active
    user_is_active.short_description = 'Active'
    user_is_active.boolean = True
    user_is_active.admin_order_field = 'user__is_active'

    def user_info(self, obj):
        if obj.user:
            return format_html(
                """
                <div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <strong>Username:</strong> {}<br>
                <strong>Email:</strong> {}<br>
                <strong>Full Name:</strong> {} {}<br>
                <strong>Staff:</strong> {} | <strong>Active:</strong> {}<br>
                <strong>Superuser:</strong> {}
                </div>
                """,
                obj.user.username,
                obj.user.email,
                obj.user.first_name,
                obj.user.last_name,
                "✓" if obj.user.is_staff else "✗",
                "✓" if obj.user.is_active else "✗",
                "✓" if obj.user.is_superuser else "✗"
            )
        return "No user associated"
    user_info.short_description = 'User Details'

    def user_permissions_display(self, obj):
        if obj.user:
            groups = obj.user.groups.all()
            permissions = obj.user.user_permissions.all()

            groups_html = ""
            if groups:
                groups_html = "<strong>Groups:</strong><ul style='margin: 5px 0;'>"
                for group in groups:
                    groups_html += f"<li>{group.name}</li>"
                groups_html += "</ul>"
            else:
                groups_html = "<strong>Groups:</strong> None<br>"

            permissions_html = ""
            if permissions:
                permissions_html = "<strong>Permissions:</strong><ul style='margin: 5px 0;'>"
                for perm in permissions[:10]:  # Show first 10 permissions
                    permissions_html += f"<li>{perm.name}</li>"
                if len(permissions) > 10:
                    permissions_html += f"<li>... and {len(permissions) - 10} more</li>"
                permissions_html += "</ul>"
            else:
                permissions_html = "<strong>Permissions:</strong> None<br>"

            return format_html(
                """
                <div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <strong>Staff Status:</strong> {}<br>
                <strong>Superuser Status:</strong> {}<br>
                <strong>Active Status:</strong> {}<br>
                {}
                {}
                </div>
                """,
                "Yes" if obj.user.is_staff else "No",
                "Yes" if obj.user.is_superuser else "No",
                "Yes" if obj.user.is_active else "No",
                groups_html,
                permissions_html
            )
        return "No user associated"
    user_permissions_display.short_description = 'Permissions Information'

    def user_important_dates(self, obj):
        if obj.user:
            return format_html(
                """
                <div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <strong>Date Joined:</strong> {}<br>
                <strong>Last Login:</strong> {}<br>
                </div>
                """,
                obj.user.date_joined.strftime("%d %b %Y %H:%M:%S"),
                obj.user.last_login.strftime("%d %b %Y %H:%M:%S") if obj.user.last_login else "Never"
            )
        return "No user associated"
    user_important_dates.short_description = 'Important Dates'

# ================================
# EXISTING HOTEL MODELS ADMIN
# ================================

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
    list_display = ['id', 'guest_name', 'room_display', 'total_guests',
                   'check_in', 'check_out', 'status', 'total_price_display', 'created_at']
    list_filter = ['status', 'check_in', 'check_out', 'created_at']
    search_fields = ['guest_name', 'guest_email', 'room__city__name',
                    'room__room_type__name']
    readonly_fields = ['created_at', 'updated_at', 'total_price_display']
    list_per_page = 20
    date_hierarchy = 'created_at'

    def room_display(self, obj):
        return str(obj.room)
    room_display.short_description = 'Room'

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
    list_per_page = 20
    search_fields = ['title', 'description']
    date_hierarchy = 'posted_date'
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

# ================================
# REGISTRATION - UPDATED VERSION
# ================================

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register all hotel models in the desired order
admin.site.register(City, CityAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)

# Register UserProfile under Rooms section
admin.site.register(UserProfile, UserProfileAdmin)

# Continue with other models
admin.site.register(Booking, BookingAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(JobListing, JobListingAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)

# Optional: Custom admin site header and title
admin.site.site_header = "ABC Hotels Administration"
admin.site.site_title = "ABC Hotels Admin Portal"
admin.site.index_title = "Welcome to ABC Hotels Administration"