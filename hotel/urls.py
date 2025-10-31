# hotel/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),
    path('book/<int:room_id>/', views.booking_form, name='booking_form'),
    path('quick-booking/', views.room_list, name='quick_booking'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('careers/', views.careers, name='careers'),
    path('careers/job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('careers/job/<int:job_id>/apply/', views.job_application, name='job_apply'),
    path('careers/why-work-with-us/', views.why_work_with_us, name='why_work_with_us'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)