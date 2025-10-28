# hotel/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('room/<int:room_type_id>/', views.room_detail, name='room_detail'),
    path('book/<int:room_id>/', views.booking_form, name='booking_form'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('quick-booking/', views.quick_booking, name='quick_booking'),
    path('faq/', views.faq, name='faq'),
    path('careers/', views.careers, name='careers'),
    path('careers/job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('careers/job/<int:job_id>/apply/', views.job_application, name='job_application'),
    path('careers/why-work-with-us/', views.why_work_with_us, name='why_work_with_us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)