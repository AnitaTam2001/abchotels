# hotel/views.py
# hotel/views.py - Update imports at the top
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from decimal import Decimal
from .models import RoomType, Room, Booking, FAQ, Department, JobListing, JobApplication
from datetime import datetime, date

# hotel/views.py - Add these imports
from .models import JobListing, Department, JobApplication
from django.core.files.storage import FileSystemStorage

def home(request):
    """Home page view"""
    room_types = RoomType.objects.all()
    return render(request, 'home.html', {'room_types': room_types})

def room_list(request):
    """Room list page view with filters"""
    room_types = RoomType.objects.all()
    
    # Get filter parameters
    room_type_filter = request.GET.get('room_type', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    capacity = request.GET.get('capacity', '')
    
    # Apply filters
    filtered_rooms = room_types
    
    if room_type_filter:
        filtered_rooms = filtered_rooms.filter(name__icontains=room_type_filter)
    
    if price_min:
        filtered_rooms = filtered_rooms.filter(price_per_night__gte=price_min)
    
    if price_max:
        filtered_rooms = filtered_rooms.filter(price_per_night__lte=price_max)
    
    if capacity:
        filtered_rooms = filtered_rooms.filter(capacity__gte=capacity)
    
    return render(request, 'room_list.html', {
        'room_types': filtered_rooms,
        'all_room_types': room_types,
        'selected_type': room_type_filter,
        'price_min': price_min,
        'price_max': price_max,
        'capacity': capacity
    })

def room_detail(request, room_type_id):
    """Room detail page view"""
    room_type = get_object_or_404(RoomType, id=room_type_id)
    available_rooms = Room.objects.filter(room_type=room_type, is_available=True)
    
    # Get similar rooms for recommendations - FIXED: Convert float to Decimal
    similar_rooms = RoomType.objects.exclude(id=room_type_id).filter(
        price_per_night__lte=room_type.price_per_night * Decimal('1.5'),
        price_per_night__gte=room_type.price_per_night * Decimal('0.5')
    )[:3]
    
    return render(request, 'room_detail.html', {
        'room_type': room_type,
        'available_rooms': available_rooms,
        'similar_rooms': similar_rooms
    })

def booking_form(request, room_id):
    """Booking form view"""
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        guest_email = request.POST.get('guest_email')
        guest_phone = request.POST.get('guest_phone')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        special_requests = request.POST.get('special_requests', '')
        
        # Validate dates
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, 'Please enter valid dates.')
            return render(request, 'booking_form.html', {'room': room})
        
        # Check if dates are valid
        today = date.today()
        if check_in_date < today:
            messages.error(request, 'Check-in date cannot be in the past.')
            return render(request, 'booking_form.html', {'room': room})
        
        if check_out_date <= check_in_date:
            messages.error(request, 'Check-out date must be after check-in date.')
            return render(request, 'booking_form.html', {'room': room})
        
        # Check room availability for the dates
        existing_bookings = Booking.objects.filter(
            room=room,
            status__in=['confirmed', 'pending'],
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        )
        
        if existing_bookings.exists():
            messages.error(request, 'Sorry, this room is not available for the selected dates.')
            return render(request, 'booking_form.html', {'room': room})
        
        # Calculate total price
        nights = (check_out_date - check_in_date).days
        total_price = nights * room.room_type.price_per_night
        
        # Create booking
        booking = Booking.objects.create(
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            total_price=total_price,
            status='pending'
        )
        
        messages.success(request, f'Booking submitted successfully! Your total is ${total_price:.2f}. We will contact you soon.')
        return redirect('home')
    
    # Set minimum date for check-in to today
    today = date.today().isoformat()
    return render(request, 'booking_form.html', {
        'room': room,
        'today': today
    })

def about(request):
    """About page view"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view"""
    # Get some common FAQs to show on contact page
    common_faqs = FAQ.objects.filter(is_active=True)[:5]
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_method = request.POST.get('contact_method', 'email')
        
        # Here you would typically save to database or send email
        messages.success(request, f'Thank you {name}! Your message has been sent. We will contact you via {contact_method} soon.')
        return redirect('contact')
    
    return render(request, 'contact.html', {
        'common_faqs': common_faqs
    })

def quick_booking(request):
    """Quick booking selection page"""
    room_types = RoomType.objects.all()
    
    # Get quick booking parameters
    check_in = request.GET.get('check_in', '')
    check_out = request.GET.get('check_out', '')
    guests = request.GET.get('guests', 1)
    
    available_rooms = RoomType.objects.all()
    
    if guests:
        available_rooms = available_rooms.filter(capacity__gte=guests)
    
    return render(request, 'quick_booking.html', {
        'room_types': available_rooms,
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests
    })

def faq(request):
    """FAQ page view"""
    categories = {
        'booking': 'Booking & Reservations',
        'rooms': 'Rooms & Amenities',
        'services': 'Hotel Services',
        'payment': 'Payment & Cancellation',
        'general': 'General Information',
    }
    
    faqs = {}
    for category_key, category_name in categories.items():
        faqs[category_name] = FAQ.objects.filter(category=category_key, is_active=True)
    
    return render(request, 'faq.html', {
        'faqs': faqs,
        'categories': categories
    })

# Add these views after the existing views
def careers(request):
    """Careers main page view"""
    departments = Department.objects.all()
    active_jobs = JobListing.objects.filter(is_active=True)
    
    # Get filter parameters
    department_filter = request.GET.get('department', '')
    job_type_filter = request.GET.get('job_type', '')
    experience_filter = request.GET.get('experience', '')
    
    # Apply filters
    if department_filter:
        active_jobs = active_jobs.filter(department__id=department_filter)
    
    if job_type_filter:
        active_jobs = active_jobs.filter(job_type=job_type_filter)
    
    if experience_filter:
        active_jobs = active_jobs.filter(experience_level=experience_filter)
    
    return render(request, 'careers.html', {
        'departments': departments,
        'active_jobs': active_jobs,
        'selected_department': department_filter,
        'selected_job_type': job_type_filter,
        'selected_experience': experience_filter,
    })

def job_detail(request, job_id):
    """Job detail page view"""
    job = get_object_or_404(JobListing, id=job_id, is_active=True)
    
    # Get related jobs in the same department
    related_jobs = JobListing.objects.filter(
        department=job.department,
        is_active=True
    ).exclude(id=job.id)[:3]
    
    return render(request, 'job_detail.html', {
        'job': job,
        'related_jobs': related_jobs,
    })

def job_application(request, job_id):
    """Job application form view"""
    job = get_object_or_404(JobListing, id=job_id, is_active=True)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cover_letter = request.POST.get('cover_letter')
        portfolio_url = request.POST.get('portfolio_url', '')
        linkedin_url = request.POST.get('linkedin_url', '')
        available_start_date = request.POST.get('available_start_date')
        expected_salary = request.POST.get('expected_salary', '')
        resume = request.FILES.get('resume')
        
        # Validate required fields
        if not all([first_name, last_name, email, phone, cover_letter, available_start_date, resume]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'job_application.html', {'job': job})
        
        # Validate file type
        allowed_types = ['.pdf', '.doc', '.docx']
        file_extension = os.path.splitext(resume.name)[1].lower()
        if file_extension not in allowed_types:
            messages.error(request, 'Please upload a PDF, DOC, or DOCX file.')
            return render(request, 'job_application.html', {'job': job})
        
        # Validate file size (5MB max)
        if resume.size > 5 * 1024 * 1024:
            messages.error(request, 'Resume file size must be less than 5MB.')
            return render(request, 'job_application.html', {'job': job})
        
        # Create application
        application = JobApplication.objects.create(
            job=job,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            cover_letter=cover_letter,
            portfolio_url=portfolio_url,
            linkedin_url=linkedin_url,
            available_start_date=available_start_date,
            expected_salary=expected_salary,
            resume=resume
        )
        
        messages.success(request, f'Thank you {first_name}! Your application for {job.title} has been submitted successfully.')
        return redirect('careers')
    
    return render(request, 'job_application.html', {'job': job})

def why_work_with_us(request):
    """Why work with us page"""
    return render(request, 'why_work_with_us.html')