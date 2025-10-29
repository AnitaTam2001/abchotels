# hotel/views.py
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from decimal import Decimal
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import City, RoomType, Room, Booking, FAQ, Department, JobListing, JobApplication
from datetime import datetime, date

def home(request):
    """Home page view"""
    cities = City.objects.filter(is_active=True)[:4]  # Show 4 featured cities
    return render(request, 'home.html', {'cities': cities})

def room_list(request):
    """City list page view with filters"""
    cities = City.objects.filter(is_active=True)

    # Get filter parameters
    city_filter = request.GET.get('city', '')
    check_in_date = request.GET.get('check_in', '')
    check_out_date = request.GET.get('check_out', '')
    guests_filter = request.GET.get('guests', '')
    rooms_filter = request.GET.get('rooms', '')

    # Apply filters
    filtered_cities = cities

    # City filter
    if city_filter:
        filtered_cities = filtered_cities.filter(name__icontains=city_filter)

    # Date availability filter
    if check_in_date and check_out_date:
        try:
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
            
            # Get cities that have available rooms for the selected dates
            cities_with_availability = []
            for city in filtered_cities:
                # Count available rooms in this city for the selected dates
                available_rooms = Room.objects.filter(
                    city=city,
                    is_available=True
                ).exclude(
                    id__in=Booking.objects.filter(
                        status__in=['confirmed', 'pending'],
                        check_in__lt=check_out,
                        check_out__gt=check_in
                    ).values_list('room_id', flat=True)
                )
                
                if available_rooms.exists():
                    cities_with_availability.append(city.id)
            
            filtered_cities = filtered_cities.filter(id__in=cities_with_availability)
            
        except (ValueError, TypeError):
            # If date parsing fails, continue without date filtering
            pass

    # Guests filter (capacity)
    if guests_filter:
        cities_with_capacity = []
        for city in filtered_cities:
            # Check if city has rooms that can accommodate the number of guests
            suitable_rooms = Room.objects.filter(
                city=city,
                room_type__capacity__gte=guests_filter,
                is_available=True
            )
            if suitable_rooms.exists():
                cities_with_capacity.append(city.id)
        
        filtered_cities = filtered_cities.filter(id__in=cities_with_capacity)

    # Rooms filter (number of available rooms)
    if rooms_filter:
        try:
            rooms_count = int(rooms_filter)
            cities_with_sufficient_rooms = []
            for city in filtered_cities:
                available_rooms_count = Room.objects.filter(
                    city=city,
                    is_available=True
                ).count()
                if available_rooms_count >= rooms_count:
                    cities_with_sufficient_rooms.append(city.id)
            
            filtered_cities = filtered_cities.filter(id__in=cities_with_sufficient_rooms)
        except ValueError:
            pass

    # Add room count and starting price to each city
    for city in filtered_cities:
        city.room_count = Room.objects.filter(city=city, is_available=True).count()
        cheapest_room = Room.objects.filter(
            city=city, 
            is_available=True
        ).select_related('room_type').order_by('room_type__price_per_night').first()
        city.starting_price = cheapest_room.room_type.price_per_night if cheapest_room else 0

    return render(request, 'room_list.html', {
        'cities': filtered_cities,
        'all_cities': City.objects.filter(is_active=True),
        'selected_city': city_filter,
        'selected_check_in': check_in_date,
        'selected_check_out': check_out_date,
        'selected_guests': guests_filter,
        'selected_rooms': rooms_filter
    })

def city_detail(request, city_id):
    """City detail page view"""
    city = get_object_or_404(City, id=city_id, is_active=True)
    
    # Get available rooms in this city
    available_rooms = Room.objects.filter(city=city, is_available=True)
    
    # Get unique room types available in this city
    room_types = RoomType.objects.filter(
        room__city=city,
        room__is_available=True
    ).distinct()
    
    # Get other active cities for recommendations
    other_cities = City.objects.filter(is_active=True).exclude(id=city_id)[:3]

    return render(request, 'city_detail.html', {
        'city': city,
        'available_rooms': available_rooms,
        'room_types': room_types,
        'other_cities': other_cities
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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_method = request.POST.get('contact_method', 'email')

        # Here you would typically save to database or send email
        messages.success(request, f'Thank you {name}! Your message has been sent. We will contact you via {contact_method} soon.')
        return redirect('contact')

    return render(request, 'contact.html')

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
        active_jobs = active_jobs.filter(department_id=department_filter)

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

        # Validate required fields - FIXED: use list for all()
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

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def profile(request):
    """User profile view"""
    # Get user's bookings
    user_bookings = Booking.objects.filter(guest_email=request.user.email)

    return render(request, 'profile.html', {
        'user_bookings': user_bookings
    })