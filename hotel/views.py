# hotel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Min
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, Http404
from datetime import datetime, date
from .models import City, RoomType, Room, Booking, FAQ, JobListing, ContactSubmission  # ADDED ContactSubmission
from django.contrib.admin.views.decorators import staff_member_required
from .forms import BookingForm, CustomUserCreationForm, ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
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

def debug_url_patterns(request):
    """Debug function to check URL patterns"""
    try:
        url = reverse('booking_confirmation', kwargs={'booking_id': 999})
        return HttpResponse(f"URL pattern works! Generated URL: {url}")
    except Exception as e:
        return HttpResponse(f"URL pattern error: {e}")

def home(request):
    featured_cities = City.objects.filter(is_active=True).annotate(
        room_count=Count('rooms', filter=Q(rooms__is_available=True))
    )[:3]
    context = {
        'featured_cities': featured_cities,
    }
    return render(request, 'home.html', context)

def room_list(request):
    all_cities = City.objects.filter(is_active=True).order_by('name')

    selected_city = request.GET.get('city', '')
    selected_check_in = request.GET.get('check_in', '')
    selected_check_out = request.GET.get('check_out', '')
    selected_guests = request.GET.get('guests', '')
    selected_rooms = request.GET.get('rooms', '')

    if selected_city:
        try:
            city = City.objects.get(name=selected_city, is_active=True)
            redirect_url = f'/cities/{city.id}/'
            params = []
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

    cities = City.objects.filter(is_active=True)
    cities = cities.annotate(
        room_count=Count('rooms', filter=Q(rooms__is_available=True)),
        starting_price=Min('rooms__room_type__price_per_night')
    ).order_by('name')

    if selected_rooms:
        min_rooms = int(selected_rooms)
        cities = cities.filter(room_count__gte=min_rooms)

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
    all_cities = City.objects.filter(is_active=True).order_by('name')

    selected_city = request.GET.get('city', '')
    selected_check_in = request.GET.get('check_in', '')
    selected_check_out = request.GET.get('check_out', '')
    selected_guests = request.GET.get('guests', '')
    selected_rooms = request.GET.get('rooms', '')

    if selected_city and selected_city != city.name:
        try:
            new_city = City.objects.get(name=selected_city, is_active=True)
            redirect_url = f"/cities/{new_city.id}/"
            params = []
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

    room_types = RoomType.objects.filter(
        room__city=city,
        room__is_available=True
    ).distinct()

    if selected_guests and selected_guests.strip():
        try:
            selected_guests_int = int(selected_guests)
            room_types = room_types.filter(capacity__gte=selected_guests_int)
        except ValueError:
            pass

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

    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    selected_guests = request.GET.get('guests', '') # Get guests from URL params

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.room = room
                booking.save()

                messages.success(request, f'Booking confirmed! Total price: ${booking.total_price}')
                return redirect('booking_confirmation', booking_id=booking.id)
            except Exception as e:
                messages.error(request, f'Error creating booking: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Pre-populate form with data from URL parameters
        initial_data = {}
        if check_in:
            initial_data['check_in'] = check_in
        if check_out:
            initial_data['check_out'] = check_out
        if selected_guests:
            try:
                initial_data['total_guests'] = int(selected_guests)
            except ValueError:
                # If guests is not a valid number, use room capacity as fallback
                initial_data['total_guests'] = room.room_type.capacity
        else:
            # Default to room capacity if no guests specified
            initial_data['total_guests'] = room.room_type.capacity

        form = BookingForm(initial=initial_data)

    # Calculate total nights and amount for display
    total_nights = 0
    total_amount = 0
    if check_in and check_out:
        try:
            from datetime import datetime
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            total_nights = (check_out_date - check_in_date).days
            total_amount = total_nights * room.room_type.price_per_night
        except ValueError:
            pass

    context = {
        'room': room,
        'form': form,
        'today': timezone.now().date(),
        'total_nights': total_nights,
        'total_amount': total_amount,
        'selected_guests': selected_guests,
    }
    return render(request, 'booking_form.html', context)

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    context = {
        'booking': booking,
    }
    return render(request, 'booking_confirmation.html', context)

@login_required
def booking_list(request):
    """View to display all bookings for the current user"""
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(guest_email=request.user.email).order_by('-created_at')
    else:
        bookings = []
    context = {
        'bookings': bookings,
    }
    return render(request, 'booking_list.html', context)

@login_required
def booking_detail(request, booking_id):
    """Detailed view of a specific booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    if not request.user.is_staff:
        if hasattr(booking, 'user') and booking.user != request.user:
            raise Http404("Booking not found")
        elif booking.guest_email != request.user.email:
            raise Http404("Booking not found")
    nights = (booking.check_out - booking.check_in).days
    price_per_night = booking.room.room_type.price_per_night
    context = {
        'booking': booking,
        'nights': nights,
        'price_per_night': price_per_night,
    }
    return render(request, 'booking_detail.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'General Inquiry')
        message = request.POST.get('message')
        
        # Validate required fields
        if not name or not email or not message:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html')
        
        try:
            # Save to database first (this will always work)
            submission = ContactSubmission.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            # Try to send emails (but don't fail the whole process if email fails)
            email_sent = False
            try:
                # Email to hotel (you)
                hotel_subject = f'📧 New Contact Form: {subject}'
                hotel_message = f"""
New contact form submission from ABC Hotels website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This email was sent from your website contact form at {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}
Submission ID: {submission.id}
"""
                
                send_mail(
                    subject=hotel_subject,
                    message=hotel_message.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                
                # Auto-reply to user
                user_subject = 'Thank you for contacting ABC Hotels'
                user_message = f"""
Dear {name},

Thank you for contacting ABC Hotels. We have received your message and our team will get back to you within 24-48 hours.

Here's a summary of your inquiry:
• Subject: {subject}
• Message: {message}

If you have any urgent inquiries, please don't hesitate to call us directly at +1 (555) 123-4567.

We look forward to assisting you with your hotel needs.

Best regards,
ABC Hotels Team
📞 +1 (555) 123-4567
📍 123 Luxury Avenue, Hospitality District
🌐 www.abchotels.com
"""
                
                send_mail(
                    subject=user_subject,
                    message=user_message.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                
                email_sent = True
                print(f"✅ Emails sent successfully for submission {submission.id}")
                
            except Exception as e:
                print(f"⚠️ Email failed but submission saved (ID: {submission.id}): {e}")
                # Continue anyway since the submission is saved to database
            
            if email_sent:
                messages.success(request, 'Thank you for your message! We have sent you a confirmation email and will get back to you soon.')
            else:
                messages.success(request, 'Thank you for your message! We have received your inquiry and will get back to you soon. (Email confirmation may be delayed)')
            
        except Exception as e:
            messages.error(request, 'Sorry, there was an error processing your message. Please try again.')
            print(f"❌ Contact form error: {e}")
        
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
        messages.success(request, 'Application submitted successfully!')
        return redirect('careers')

    context = {
        'job': job,
    }
    return render(request, 'job_application.html', context)

def why_work_with_us(request):
    return render(request, 'why_work_with_us.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(guest_email=request.user.email)
    else:
        bookings = []

    context = {
        'bookings': bookings,
    }
    return render(request, 'dashboard.html', context)

@staff_member_required
def room_admin(request):
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

@login_required
def profile(request):
    # Show all bookings by default
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(guest_email=request.user.email).order_by('-created_at')
    else:
        user_bookings = []
    context = {
        'user_bookings': user_bookings,
        'show_all': True  # Flag to indicate showing all bookings
    }
    return render(request, 'profile.html', context)

@login_required
def current_bookings(request):
    # Show only current/future bookings
    today = timezone.now().date()
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(
            guest_email=request.user.email,
            check_out__gte=today  # Only bookings that haven't ended
        ).order_by('-created_at')
    else:
        user_bookings = []
    context = {
        'user_bookings': user_bookings,
        'show_all': False  # Flag to indicate showing current bookings only
    }
    return render(request, 'profile.html', context)

@login_required
def account_settings(request):
    """View for user account settings"""
    return render(request, 'account_settings.html')