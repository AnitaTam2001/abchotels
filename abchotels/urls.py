# abchotels/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from hotel import views as hotel_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hotel_views.home, name='home'),
    path('about/', hotel_views.about, name='about'),
    path('contact/', hotel_views.contact, name='contact'),
    path('rooms/', hotel_views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', hotel_views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', hotel_views.booking_form, name='booking_form'),
    path('booking/confirmation/', hotel_views.booking_confirmation, name='booking_confirmation'),
    path('cities/<int:city_id>/', hotel_views.city_detail, name='city_detail'),
    path('faq/', hotel_views.faq, name='faq'),
    path('careers/', hotel_views.careers, name='careers'),
    path('careers/why-work-with-us/', hotel_views.why_work_with_us, name='why_work_with_us'),
    path('careers/<int:job_id>/', hotel_views.job_detail, name='job_detail'),
    path('careers/<int:job_id>/apply/', hotel_views.job_application, name='job_application'),
    path('dashboard/', hotel_views.dashboard, name='dashboard'),
    path('profile/', hotel_views.profile, name='profile'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', hotel_views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)