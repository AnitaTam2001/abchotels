# hotel/management/commands/seed_jobs.py
from django.core.management.base import BaseCommand
from hotel.models import Department, JobListing
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample job listings'

    def handle(self, *args, **options):
        # Clear existing data
        Department.objects.all().delete()
        JobListing.objects.all().delete()

        # Create departments
        departments_data = [
            {'name': 'Front Office', 'description': 'Guest services and front desk operations'},
            {'name': 'Food & Beverage', 'description': 'Restaurant, bar, and catering services'},
            {'name': 'Housekeeping', 'description': 'Room cleaning and maintenance'},
            {'name': 'Sales & Marketing', 'description': 'Business development and promotional activities'},
            {'name': 'Human Resources', 'description': 'Employee management and development'},
            {'name': 'Finance & Accounting', 'description': 'Financial operations and reporting'},
            {'name': 'Engineering', 'description': 'Facility maintenance and technical operations'},
            {'name': 'Security', 'description': 'Safety and security operations'},
        ]

        departments = {}
        for dept_data in departments_data:
            department = Department.objects.create(**dept_data)
            departments[dept_data['name']] = department
            self.stdout.write(
                self.style.SUCCESS(f'Created department: {department.name}')
            )

        # Create sample job listings
        jobs_data = [
            {
                'title': 'Front Desk Agent',
                'department': departments['Front Office'],
                'job_type': 'full_time',
                'experience_level': 'entry',
                'location': 'Main Hotel',
                'salary_range': '$35,000 - $45,000',
                'description': 'We are seeking a friendly and professional Front Desk Agent to join our team. The ideal candidate will be the first point of contact for our guests and will play a crucial role in creating exceptional guest experiences.',
                'requirements': '''• High school diploma or equivalent
• Excellent communication and customer service skills
• Ability to handle multiple tasks simultaneously
• Basic computer proficiency
• Flexible schedule including weekends and holidays''',
                'responsibilities': '''• Greet and check-in guests upon arrival
• Handle guest inquiries and resolve issues
• Process payments and maintain accurate records
• Coordinate with other departments to ensure guest satisfaction
• Maintain knowledge of hotel services and local attractions''',
                'benefits': '''• Health, dental, and vision insurance
• 401(k) with company matching
• Paid time off and holidays
• Employee hotel discounts
• Career development opportunities''',
                'application_deadline': date.today() + timedelta(days=30)
            },
            {
                'title': 'Executive Chef',
                'department': departments['Food & Beverage'],
                'job_type': 'full_time',
                'experience_level': 'senior',
                'location': 'Main Hotel',
                'salary_range': '$75,000 - $95,000',
                'description': 'We are looking for an experienced and creative Executive Chef to lead our culinary team. The ideal candidate will have a passion for culinary excellence and a proven track record in hotel or fine dining environments.',
                'requirements': '''• Culinary degree or equivalent experience
• 8+ years of culinary experience, with 3+ years in leadership
• Extensive knowledge of various cuisines and cooking techniques
• Strong leadership and team management skills
• Food safety certification''',
                'responsibilities': '''• Oversee all kitchen operations and staff
• Develop and update menus seasonally
• Maintain food quality and presentation standards
• Control food and labor costs
• Train and mentor kitchen staff''',
                'benefits': '''• Competitive salary and bonus structure
• Comprehensive benefits package
• Creative freedom in menu development
• Professional development opportunities
• Relocation assistance available''',
                'application_deadline': date.today() + timedelta(days=45)
            },
            {
                'title': 'Sales Manager',
                'department': departments['Sales & Marketing'],
                'job_type': 'full_time',
                'experience_level': 'mid',
                'location': 'Main Hotel',
                'salary_range': '$60,000 - $75,000 + Commission',
                'description': 'We are seeking a dynamic Sales Manager to drive group and corporate sales. The ideal candidate will have a proven ability to build relationships and exceed sales targets in the hospitality industry.',
                'requirements': '''• Bachelor\'s degree in Business or related field
• 3+ years of hotel sales experience
• Proven track record of meeting sales targets
• Excellent negotiation and presentation skills
• Knowledge of hotel sales software''',
                'responsibilities': '''• Develop and maintain corporate accounts
• Generate group business leads
• Prepare and present sales proposals
• Attend industry events and trade shows
• Collaborate with marketing on promotional activities''',
                'benefits': '''• Competitive base salary + commission
• Health and wellness benefits
• Company vehicle or allowance
• Professional development budget
• Performance-based bonuses''',
                'application_deadline': date.today() + timedelta(days=25)
            },
            {
                'title': 'Housekeeping Supervisor',
                'department': departments['Housekeeping'],
                'job_type': 'full_time',
                'experience_level': 'mid',
                'location': 'Main Hotel',
                'salary_range': '$40,000 - $50,000',
                'description': 'We are looking for a detail-oriented Housekeeping Supervisor to oversee our housekeeping team and ensure the highest standards of cleanliness and guest satisfaction.',
                'requirements': '''• 2+ years of housekeeping experience
• 1+ year in a supervisory role preferred
• Knowledge of cleaning procedures and chemicals
• Strong organizational and leadership skills
• Ability to work flexible hours''',
                'responsibilities': '''• Supervise and train housekeeping staff
• Inspect rooms and public areas for cleanliness
• Manage inventory and supplies
• Coordinate with maintenance for repairs
• Ensure compliance with safety standards''',
                'benefits': '''• Health insurance benefits
• Paid time off
• Employee meal program
• Career advancement opportunities
• Supportive work environment''',
                'application_deadline': date.today() + timedelta(days=20)
            },
            {
                'title': 'HR Coordinator',
                'department': departments['Human Resources'],
                'job_type': 'full_time',
                'experience_level': 'entry',
                'location': 'Corporate Office',
                'salary_range': '$45,000 - $55,000',
                'description': 'We are seeking an HR Coordinator to support our human resources department in various administrative functions and employee relations activities.',
                'requirements': '''• Bachelor\'s degree in HR or related field
• 1+ years of HR experience preferred
• Knowledge of HR laws and regulations
• Excellent organizational skills
• Proficiency in HR software''',
                'responsibilities': '''• Assist with recruitment and onboarding
• Maintain employee records
• Coordinate training programs
• Support benefits administration
• Assist with employee relations''',
                'benefits': '''• Comprehensive benefits package
• Professional development opportunities
• Flexible work arrangements
• Wellness programs
• Collaborative team environment''',
                'application_deadline': date.today() + timedelta(days=35)
            },
        ]

        for job_data in jobs_data:
            JobListing.objects.create(**job_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created job: {job_data["title"]}')
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample job listings!')
        )