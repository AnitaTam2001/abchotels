# hotel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

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

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_method = request.POST.get('contact_method', 'email')

        messages.success(request, f'Thank you {name}! Your message has been sent. We will contact you via {contact_method} soon.')
        return redirect('contact')

    return render(request, 'contact.html')

def faq(request):
    """FAQ page view"""
    return render(request, 'faq.html')

def room_list(request):
    """Room list page view"""
    return render(request, 'room_list.html')

# Add these to your existing hotel/views.py

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