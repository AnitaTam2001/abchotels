# hotel/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/<int:room_id>/', views.booking_form, name='booking_form'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/admin/', views.room_admin, name='room_admin'),
    path('cities/<int:city_id>/', views.city_detail, name='city_detail'),
    path('room-types/<int:room_type_id>/', views.room_type_detail, name='room_type_detail'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('careers/', views.careers, name='careers'),
    path('careers/<int:job_id>/', views.job_detail, name='job_detail'),
    path('careers/<int:job_id>/apply/', views.job_application, name='job_application'),
    path('why-work-with-us/', views.why_work_with_us, name='why_work_with_us'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)