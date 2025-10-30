import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from hotel.models import JobListing, Department

class Command(BaseCommand):
    help = 'Import job listings from jobs.csv'

    def handle(self, *args, **options):
        csv_file_path = 'csv/jobs.csv'
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR('CSV file not found at csv/jobs.csv'))
            return

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            jobs_created = 0
            jobs_updated = 0
            
            for row in csv_reader:
                try:
                    # Convert is_active string to boolean
                    is_active = row['is_active'].strip() == '1'
                    
                    # Get or create department
                    department_name = row['department']
                    department, _ = Department.objects.get_or_create(
                        name=department_name,
                        defaults={'description': f'{department_name} Department'}
                    )
                    
                    # Parse application deadline
                    application_deadline = datetime.strptime(row['application_deadline'], '%Y-%m-%d').date()
                    
                    # Create or update job
                    job, created = JobListing.objects.update_or_create(
                        id=row['id'],
                        defaults={
                            'title': row['title'],
                            'department': department,
                            'location': row['location'],
                            'description': row['description'],
                            'requirements': row['requirements'],
                            'employment_type': row['employment_type'],
                            'salary_range': row['salary_range'],
                            'is_active': is_active,
                            'application_deadline': application_deadline
                        }
                    )
                    
                    if created:
                        jobs_created += 1
                        self.stdout.write(f'✅ Created job: {job.title} (ID: {job.id})')
                    else:
                        jobs_updated += 1
                        self.stdout.write(f'📝 Updated job: {job.title} (ID: {job.id})')
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error with {row.get("title", "unknown")}: {e}')
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed {jobs_created + jobs_updated} jobs '
                    f'({jobs_created} created, {jobs_updated} updated)'
                )
            )