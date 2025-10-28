# hotel/management/commands/seed_faqs.py
from django.core.management.base import BaseCommand
from hotel.models import FAQ

class Command(BaseCommand):
    help = 'Seed the database with sample FAQs'

    def handle(self, *args, **options):
        # Clear existing FAQs
        FAQ.objects.all().delete()

        sample_faqs = [
            # Booking & Reservations
            {
                'question': 'What is your check-in and check-out time?',
                'answer': 'Check-in time is 3:00 PM and check-out time is 11:00 AM. Early check-in and late check-out may be available upon request and subject to availability.',
                'category': 'booking',
                'order': 1
            },
            {
                'question': 'Can I modify or cancel my reservation?',
                'answer': 'Yes, you can modify or cancel your reservation up to 24 hours before your check-in date without any charges. Please contact our reservations team for assistance.',
                'category': 'booking',
                'order': 2
            },
            {
                'question': 'Do you offer early check-in or late check-out?',
                'answer': 'Early check-in and late check-out are subject to availability and may involve additional charges. Please contact us in advance to arrange.',
                'category': 'booking',
                'order': 3
            },
            {
                'question': 'What is your minimum age requirement for booking?',
                'answer': 'Guests must be at least 18 years old to make a reservation. Valid government-issued photo identification is required at check-in.',
                'category': 'booking',
                'order': 4
            },

            # Rooms & Amenities
            {
                'question': 'What amenities are included in the rooms?',
                'answer': 'All rooms include free WiFi, flat-screen TV, mini-refrigerator, coffee maker, iron and ironing board, safe, and premium toiletries. Higher category rooms include additional amenities.',
                'category': 'rooms',
                'order': 1
            },
            {
                'question': 'Do your rooms have air conditioning?',
                'answer': 'Yes, all our rooms are equipped with individual climate control systems for your comfort.',
                'category': 'rooms',
                'order': 2
            },
            {
                'question': 'Are the rooms non-smoking?',
                'answer': 'Yes, all our rooms and indoor areas are strictly non-smoking. Designated smoking areas are available outside the hotel.',
                'category': 'rooms',
                'order': 3
            },
            {
                'question': 'Do you have connecting rooms for families?',
                'answer': 'Yes, we offer connecting rooms for families. Please mention this requirement when making your reservation.',
                'category': 'rooms',
                'order': 4
            },

            # Hotel Services
            {
                'question': 'Do you have parking facilities?',
                'answer': 'Yes, we offer both valet parking and self-parking options. Parking fees apply and reservations are recommended.',
                'category': 'services',
                'order': 1
            },
            {
                'question': 'Is breakfast included in the room rate?',
                'answer': 'Breakfast is not automatically included but can be added to your reservation. We offer various breakfast packages to suit your needs.',
                'category': 'services',
                'order': 2
            },
            {
                'question': 'Do you have a swimming pool and fitness center?',
                'answer': 'Yes, we have an outdoor swimming pool and a fully equipped fitness center available to all guests free of charge.',
                'category': 'services',
                'order': 3
            },
            {
                'question': 'Is room service available?',
                'answer': 'Yes, room service is available from 6:00 AM to 11:00 PM daily. Our menu features a variety of local and international dishes.',
                'category': 'services',
                'order': 4
            },

            # Payment & Cancellation
            {
                'question': 'What payment methods do you accept?',
                'answer': 'We accept all major credit cards (Visa, MasterCard, American Express), debit cards, and cash. Corporate accounts and wire transfers are also accepted.',
                'category': 'payment',
                'order': 1
            },
            {
                'question': 'Do you require a security deposit?',
                'answer': 'Yes, we require a security deposit of $100 per room upon check-in. This will be refunded upon check-out after room inspection.',
                'category': 'payment',
                'order': 2
            },
            {
                'question': 'What is your cancellation policy?',
                'answer': 'Cancellations made 24 hours or more before check-in are free. Cancellations within 24 hours may incur one night\'s room charge.',
                'category': 'payment',
                'order': 3
            },

            # General Information
            {
                'question': 'Do you have facilities for guests with disabilities?',
                'answer': 'Yes, we have wheelchair-accessible rooms and facilities. Please inform us of any specific requirements when booking.',
                'category': 'general',
                'order': 1
            },
            {
                'question': 'Are pets allowed in the hotel?',
                'answer': 'We welcome service animals. For pets, we have limited pet-friendly rooms available with prior arrangement. Additional charges and policies apply.',
                'category': 'general',
                'order': 2
            },
            {
                'question': 'Do you offer airport transportation?',
                'answer': 'Yes, we offer airport shuttle service for an additional fee. Advance reservation is required.',
                'category': 'general',
                'order': 3
            },
            {
                'question': 'Is there a business center?',
                'answer': 'Yes, we have a 24-hour business center with computers, printers, and meeting rooms available for guest use.',
                'category': 'general',
                'order': 4
            },
        ]

        for faq_data in sample_faqs:
            FAQ.objects.create(**faq_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created FAQ: {faq_data["question"]}')
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample FAQs!')
        )