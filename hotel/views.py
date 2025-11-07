# hotel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .models import City
# hotel/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def room_list(request):
    cities = City.objects.all()
    all_cities = City.objects.all()  # For the filter dropdown

    # Get filter parameters
    selected_city = request.GET.get('city', '')
    selected_check_in = request.GET.get('check_in', '')
    selected_check_out = request.GET.get('check_out', '')
    selected_guests = request.GET.get('guests', '')
    selected_rooms = request.GET.get('rooms', '')

    # Apply filters
    if selected_city:
        cities = cities.filter(name__icontains=selected_city)

    # Pagination - 12 items per page
    paginator = Paginator(cities, 12)
    page_number = request.GET.get('page')
    
    try:
        paginated_cities = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_cities = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_cities = paginator.page(paginator.num_pages)

    context = {
        'cities': paginated_cities,  # Use paginated queryset
        'all_cities': all_cities,
        'selected_city': selected_city,
        'selected_check_in': selected_check_in,
        'selected_check_out': selected_check_out,
        'selected_guests': selected_guests,
        'selected_rooms': selected_rooms,
        'paginator': paginator,  # Add paginator to context
    }

    return render(request, 'room_list.html', context)

def register(request):
    """
    User registration view for ABC Hotels
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use custom form
        if form.is_valid():
            # Save the user
            user = form.save()

            # Auto-login after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Account created successfully! Welcome, {username}!')
                return redirect('dashboard')
        else:
            # Form has errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()  # Use custom form
    
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    """
    Custom login view for ABC Hotels
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login successful
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            
            # Redirect to next page or dashboard
            next_page = request.GET.get('next', 'dashboard')
            return redirect(next_page)
        else:
            # Login failed
            messages.error(request, 'Invalid username or password. Please try again.')
    
    # If GET request or failed login, show login page
    return render(request, 'registration/login.html')

def user_logout(request):
    """
    Logout view
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

@login_required
def dashboard(request):
    """
    Dashboard view - requires login
    """
    return render(request, 'dashboard.html', {'user': request.user})

@login_required
def profile(request):
    """
    User profile view
    """
    return render(request, 'profile.html', {'user': request.user})

def home(request):
    """Home page view"""
    return render(request, 'home.html')

def about(request):
    """About page view"""
    return render(request, 'about.html')

# hotel/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings

def contact(request):
    """Contact page view with email functionality"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_method = request.POST.get('contact_method', 'email')
        
        # Prepare email content
        email_subject = f"Contact Form: {subject}"
        email_message = f"""
        New contact form submission from ABC Hotels website:
        
        Name: {name}
        Email: {email}
        Preferred Contact Method: {contact_method}
        
        Message:
        {message}
        
        This message was sent from the contact form on ABC Hotels website.
        """
        
        try:
            # Send email to hotel
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,  # From email
                ['anitatam2001@gmail.com'],
#               ['info@abchotels.com'],  
#               To email - change to your hotel's email
                fail_silently=False,
            )
            
            # Send confirmation email to user
            confirmation_subject = "Thank you for contacting ABC Hotels"
            confirmation_message = f"""
            Dear {name},
            
            Thank you for contacting ABC Hotels. We have received your message and will get back to you within 24 hours.
            
            Here's a summary of your inquiry:
            Subject: {subject}
            Preferred Contact Method: {contact_method}
            
            Our team will contact you using your preferred method soon.
            
            Best regards,
            ABC Hotels Team
            """
            
            send_mail(
                confirmation_subject,
                confirmation_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],  # Send to the user who filled the form
                fail_silently=False,
            )
            
            messages.success(request, f'Thank you {name}! Your message has been sent. We will contact you via {contact_method} soon.')
            
        except BadHeaderError:
            messages.error(request, 'Invalid header found. Please try again.')
        except Exception as e:
            messages.error(request, f'There was an error sending your message. Please try again later. Error: {str(e)}')
        
        return redirect('contact')
    
    return render(request, 'contact.html')

def faq(request):
    """FAQ page view"""
    return render(request, 'faq.html')

def city_detail(request, city_id):
    """City detail page view"""
    return render(request, 'city_detail.html')

def booking_form(request, room_id):
    """Booking form view"""
    return render(request, 'booking_form.html')

def careers(request):
    """Careers page view"""
    return render(request, 'careers.html')

def job_detail(request, job_id):
    """Job detail page view"""
    return render(request, 'job_detail.html')

def job_application(request, job_id):
    """Job application form view"""
    return render(request, 'job_application.html')

def why_work_with_us(request):
    """Why work with us page"""
    return render(request, 'why_work_with_us.html')

def room_detail(request, room_type_id):
    """Room type detail page"""
    return render(request, 'room_detail.html')
