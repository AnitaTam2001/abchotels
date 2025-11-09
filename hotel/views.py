# hotel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Min
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from datetime import datetime, date
from .models import City, RoomType, Room, Booking, FAQ, JobListing
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    featured_cities = City.objects.filter(is_active=True).annotate(
        room_count=Count('rooms', filter=Q(rooms__is_available=True))  # Fixed: rooms__is_available
    )[:3]
    context = {
        'featured_cities': featured_cities,
    }
    return render(request, 'home.html', context)

def room_list(request):
    # Get all active cities for the filter dropdown - ORDER BY NAME ASCENDING
    all_cities = City.objects.filter(is_active=True).order_by('name')

    # Get filter parameters
    selected_city = request.GET.get('city', '')
    selected_check_in = request.GET.get('check_in', '')
    selected_check_out = request.GET.get('check_out', '')
    selected_guests = request.GET.get('guests', '')
    selected_rooms = request.GET.get('rooms', '')

    # Start with all active cities
    cities = City.objects.filter(is_active=True)

    # Apply filters
    if selected_city:
        cities = cities.filter(name__icontains=selected_city)

    # Annotate with room count and starting price
    cities = cities.annotate(
        room_count=Count('rooms', filter=Q(rooms__is_available=True)),  # Fixed: rooms__is_available
        starting_price=Min('rooms__room_type__price_per_night')  # Fixed: rooms__room_type__price_per_night
    ).order_by('name')

    # Filter by minimum room count if specified
    if selected_rooms:
        min_rooms = int(selected_rooms)
        cities = cities.filter(room_count__gte=min_rooms)

    # Pagination
    paginator = Paginator(cities, 12)
    page_number = request.GET.get('page')
    cities_page = paginator.get_page(page_number)

    context = {
        'cities': cities_page,
        'all_cities': all_cities,
        'selected_city': selected_city,
        'selected_check_in': selected_check_in,
        'selected_check_out': selected_check_out,
        'selected_guests': selected_guests,
        'selected_rooms': selected_rooms,
    }
    return render(request, 'room_list.html', context)

def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id, is_active=True)

    # Get filter parameters for the city-specific filter
    selected_check_in = request.GET.get('check_in', '')
    selected_check_out = request.GET.get('check_out', '')
    selected_guests = request.GET.get('guests', '')
    selected_rooms = request.GET.get('rooms', '')

    # Get available room types for this city
    room_types = RoomType.objects.filter(
        rooms__city=city,  # Fixed: rooms__city
        rooms__is_available=True  # Fixed: rooms__is_available
    ).distinct()

    # Apply room type filters based on capacity
    if selected_guests:
        room_types = room_types.filter(capacity__gte=int(selected_guests))

    # Get other cities for the "Explore Other Destinations" section - ORDER BY NAME
    other_cities = City.objects.filter(
        is_active=True
    ).exclude(id=city_id).annotate(
        room_count=Count('rooms', filter=Q(rooms__is_available=True))  # Fixed: rooms__is_available
    ).order_by('name')[:6]

    context = {
        'city': city,
        'room_types': room_types,
        'other_cities': other_cities,
        'selected_check_in': selected_check_in,
        'selected_check_out': selected_check_out,
        'selected_guests': selected_guests,
        'selected_rooms': selected_rooms,
        'today': date.today().isoformat(),
    }
    return render(request, 'city_detail.html', context)

def room_type_detail(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)

    # Get available rooms of this type
    available_rooms = Room.objects.filter(
        room_type=room_type,
        is_available=True
    )
    context = {
        'room_type': room_type,
        'available_rooms': available_rooms,
        'today': date.today().isoformat(),
    }
    return render(request, 'room_type_detail.html', context)

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)

    # Get similar rooms for recommendations
    similar_rooms = Room.objects.filter(
        room_type=room.room_type,
        is_available=True
    ).exclude(id=room_id)[:4]

    context = {
        'room': room,
        'similar_rooms': similar_rooms,
        'today': date.today().isoformat(),
    }
    return render(request, 'room_detail.html', context)

def booking_form(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)

    if request.method == 'POST':
        # Process booking form
        guest_name = request.POST.get('guest_name')
        guest_email = request.POST.get('guest_email')
        guest_phone = request.POST.get('guest_phone')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        # Validate dates
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

            if check_in_date >= check_out_date:
                messages.error(request, 'Check-out date must be after check-in date.')
            elif check_in_date < date.today():
                messages.error(request, 'Check-in date cannot be in the past.')
            else:
                # Calculate total price
                nights = (check_out_date - check_in_date).days
                total_price = room.room_type.price_per_night * nights

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
                # Mark room as unavailable
                room.is_available = False
                room.save()

                messages.success(request, f'Booking confirmed! Your booking reference is #{booking.id}')
                return redirect('home')

        except ValueError:
            messages.error(request, 'Invalid date format.')

    context = {
        'room': room,
        'today': date.today().isoformat(),
    }
    return render(request, 'booking_form.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        # Process contact form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Here you would typically send an email
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')

    return render(request, 'contact.html')

def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    context = {
        'faqs': faqs,
    }
    return render(request, 'faq.html', context)

def careers(request):
    job_listings = JobListing.objects.filter(is_active=True)
    context = {
        'job_listings': job_listings,
    }
    return render(request, 'careers.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id, is_active=True)
    context = {
        'job': job,
    }
    return render(request, 'job_detail.html', context)

def job_application(request, job_id):
    job = get_object_or_404(JobListing, id=job_id, is_active=True)

    if request.method == 'POST':
        # Process job application form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cover_letter = request.POST.get('cover_letter')

        # Here you would typically save the application and handle file uploads
        messages.success(request, f'Thank you for applying to {job.title}! We will review your application.')
        return redirect('careers')

    context = {
        'job': job,
    }
    return render(request, 'job_application.html', context)

def why_work_with_us(request):
    return render(request, 'why_work_with_us.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def dashboard(request):
    # Get user's bookings if user is authenticated
    if request.user.is_authenticated:
        # This would need to be adjusted based on your user-booking relationship
        bookings = Booking.objects.filter(guest_email=request.user.email)
    else:
        bookings = []

    context = {
        'bookings': bookings,
    }
    return render(request, 'dashboard.html', context)

@staff_member_required
def room_admin(request):
    """Custom admin interface for rooms management"""
    rooms = Room.objects.all().select_related('city', 'room_type')
    cities = City.objects.all()
    room_types = RoomType.objects.all()
    
    # Count available rooms
    available_rooms = rooms.filter(is_available=True).count()

    context = {
        'rooms': rooms,
        'cities': cities,
        'room_types': room_types,
        'total_rooms': rooms.count(),
        'available_rooms': available_rooms,
        'occupied_rooms': rooms.count() - available_rooms,
    }
    return render(request, 'hotel/room_admin.html', context)