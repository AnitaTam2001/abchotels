# hotel/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('room/<int:room_type_id>/', views.room_detail, name='room_detail'),
    path('book/<int:room_id>/', views.booking_form, name='booking_form'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('quick-booking/', views.quick_booking, name='quick_booking'),  # Add this line
]