# hotel/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Add UserProfile model at the top
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone_number = models.IntegerField(
        blank=True, 
        null=True, 
        help_text="8-digit phone number"
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)

# Your existing models below
class City(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/city/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class RoomType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/room/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Room(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/room_specific/', blank=True,
    null=True, verbose_name='Room Specific Image')

    def __str__(self):
        return f"{self.room_type.name} - {self.city.name}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]

    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
    related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
    default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Booking {self.id} - {self.guest_name} - {self.room}'

    @property
    def total_price(self):
        if self.check_in and self.check_out and self.room:
            nights = (self.check_out - self.check_in).days
            return nights * self.room.room_type.price_per_night
        return 0

    @property
    def nights(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 0

    class Meta:
        ordering = ['-created_at']

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('booking', 'Booking'),
        ('payment', 'Payment'),
        ('facilities', 'Facilities'),
        ('cancellation', 'Cancellation'),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,
    default='general')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order', 'category']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

class JobListing(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
    ]

    EXPERIENCE_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive'),
    ]

    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
    related_name='job_listings')
    description = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.department.name}"

    class Meta:
        ordering = ['-posted_date']

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]

    job = models.ForeignKey(JobListing, on_delete=models.CASCADE,
    related_name='applications')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
    default='applied')
    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title}"

    class Meta:
        ordering = ['-applied_date']