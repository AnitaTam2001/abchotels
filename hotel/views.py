# hotel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Min
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import datetime, date
from .models import City, RoomType, Room, Booking, FAQ, JobListing
from django.contrib.admin.views.decorators import staff_member_required
from .forms import BookingForm, CustomUserCreationForm

def home(request):
    featured_cities = City.objects.filter(is_active=True).annotate(
        room_count=Count('rooms', filter=Q(rooms__is_available=True))
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

    # If we have a city selected with filters, redirect directly to that city's page
    if selected_city:
        try:
            city = City.objects.get(name=selected_city, is_active=True)
            # Build redirect URL with all filters
            redirect_url = f'/cities/{city.id}/'
            params = []
            # Include the selected city in the parameters
            params.append(f'city={selected_city}')
            if selected_check_in:
                params.append(f'check_in={selected_check_in}')
            if selected_check_out:
                params.append(f'check_out={selected_check_out}')
            if selected_guests:
                params.append(f'guests={selected_guests}')
            if selected_rooms:
                params.append(f'rooms={selected_rooms}')
            
            if params:
                redirect_url += "?" + "&".join(params)
            return redirect(redirect_url)
        except City.DoesNotExist:
            pass

    # If no city selected or city doesn't exist, show the room list page with cities
    # Start with all active cities
    cities = City.objects.filter(is_active=True)

    # Apply filters
    if selected_city:
        cities = cities.filter(name__icontains=selected_city)

    # Annotate with room count and starting price
    cities = cities.annotate(
        room_count=Count('rooms', filter=Q(rooms__is_available=True)),
        starting_price=Min('rooms__room_type__price_per_night')
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
        'today': date.today().isoformat(),
    }
    return render(request, 'room_list.html', context)

def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id, is_active=True)

    # Get all cities for the filter dropdown - ORDER BY NAME ASCENDING
    all_cities = City.objects.filter(is_active=True).order_by('name')

    # Get filter parameters for the city-specific filter
    selected_city = request.GET.get('city', '')
    selected_check_in = request.GET.get('check_in', '')
    selected_check_out = request.GET.get('check_out', '')
    selected_guests = request.GET.get('guests', '')
    selected_rooms = request.GET.get('rooms', '')

    # If a different city is selected, redirect to that city's page with all filters
    if selected_city and selected_city != city.name:
        try:
            new_city = City.objects.get(name=selected_city, is_active=True)
            # Build redirect URL with all current filters
            redirect_url = f"/cities/{new_city.id}/"
            params = []
            # Include the selected city in the parameters for the new page
            params.append(f"city={selected_city}")
            if selected_check_in:
                params.append(f"check_in={selected_check_in}")
            if selected_check_out:
                params.append(f"check_out={selected_check_out}")
            if selected_guests:
                params.append(f"guests={selected_guests}")
            if selected_rooms:
                params.append(f"rooms={selected_rooms}")
            if params:
                redirect_url += "?" + "&".join(params)
            return redirect(redirect_url)
        except City.DoesNotExist:
            pass

    # Get available room types for this city
    room_types = RoomType.objects.filter(
        room__city=city,
        room__is_available=True
    ).distinct()

    # Apply room type filters based on capacity
    if selected_guests and selected_guests.strip():
        try:
            selected_guests_int = int(selected_guests)
            # Only show room types that can accommodate the selected number of guests
            room_types = room_types.filter(capacity__gte=selected_guests_int)
        except ValueError:
            pass

    # Get available room IDs for each room type
    room_type_data = []
    for room_type in room_types:
        available_room = Room.objects.filter(
            room_type=room_type,
            city=city,
            is_available=True
        ).first()
        room_type_data.append({
            'room_type': room_type,
            'available_room_id': available_room.id if available_room else None
        })

    # Get other cities for the "Explore Other Destinations" section
    other_cities = City.objects.filter(
        is_active=True
    ).exclude(id=city_id).annotate(
        room_count=Count('rooms', filter=Q(rooms__is_available=True))
    ).order_by('name')[:6]

    context = {
        'city': city,
        'all_cities': all_cities,
        'room_type_data': room_type_data,
        'other_cities': other_cities,
        'selected_check_in': selected_check_in,
        'selected_check_out': selected_check_out,
        'selected_guests': selected_guests,
        'selected_rooms': selected_rooms,
        'selected_city': selected_city,
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

# In hotel/views.py - fix the booking_form function
def booking_form(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Get dates from URL parameters
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                # Create booking but don't save yet
                booking = form.save(commit=False)
                booking.room = room
                booking.save()

                messages.success(request, f'Booking confirmed! Total price: ${booking.total_price}')
                # FIXED: Make sure booking_id is passed correctly
                return redirect('booking_confirmation', booking_id=booking.id)

            except Exception as e:
                messages.error(request, f'Error creating booking: {str(e)}')
        else:
            # Form is invalid, show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # GET request - create form with initial data from URL parameters
        initial_data = {}
        if check_in:
            initial_data['check_in'] = check_in
        if check_out:
            initial_data['check_out'] = check_out

        form = BookingForm(initial=initial_data)

    context = {
        'room': room,
        'form': form,
        'today': timezone.now().date(),
    }
    return render(request, 'booking_form.html', context)


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    context = {
        'booking': booking,
    }
    return render(request, 'booking_confirmation.html', context)

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
        # Add more processing as needed
        
        messages.success(request, 'Application submitted successfully!')
        return redirect('careers')

    context = {
        'job': job,
    }
    return render(request, 'job_application.html', context)

def why_work_with_us(request):
    return render(request, 'why_work_with_us.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
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
    available_rooms = rooms.filter(is_available=True)

    context = {
        'rooms': rooms,
        'cities': cities,
        'room_types': room_types,
        'available_rooms': available_rooms,
        'occupied_rooms': rooms.count() - available_rooms.count(),
    }
    return render(request, 'hotel/room_admin.html', context)