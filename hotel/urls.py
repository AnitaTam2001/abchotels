# hotel/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('careers/', views.careers, name='careers'),
    path('why-work-with-us/', views.why_work_with_us, name='why_work_with_us'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.job_application, name='job_application'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Rooms and bookings
    path('rooms/', views.room_list, name='room_list'),
    path('cities/<int:city_id>/', views.city_detail, name='city_detail'),
    path('room-types/<int:room_type_id>/', views.room_type_detail, name='room_type_detail'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', views.booking_form, name='booking_form'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    
    # User dashboard and bookings
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    
    # Admin
    path('room-admin/', views.room_admin, name='room_admin'),
    
    # Debug
    path('debug-urls/', views.debug_url_patterns, name='debug_urls'),
]