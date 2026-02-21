from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from educoach.models import Coach, CoachingSession, CoachAvailabilityRange
from datetime import datetime, timedelta, time
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample Coaches, Availability, and Booking Sessions'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Clearing existing coach availability and sessions...'))
        
        # Disconnect notification signals to prevent Email API failures during test
        try:
            from django.db.models.signals import post_save
            from notifications.signals import session_notification_signal
            post_save.disconnect(session_notification_signal, sender=CoachingSession)
        except ImportError:
            pass

        CoachAvailabilityRange.objects.all().delete()
        CoachingSession.objects.all().delete()
        
        # 1. Create or get some Student users
        student_names = ['Alice Student', 'Bob Learner', 'Charlie Pupil']
        students = []
        for name in student_names:
            username = name.replace(' ', '').lower()
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com', 'role': 'STUDENT', 'first_name': name.split()[0], 'last_name': name.split()[1]}
            )
            if created:
                user.set_password('password123')
                user.save()
            students.append(user)

        # 2. Create or get Coaches
        coach_data = [
            {'name': 'Dr. Sarah Nabirye', 'title': 'Senior Mathematics Expert', 'price': 50000, 'exp': '10 Years'},
            {'name': 'Mr. John Otim', 'title': 'Physics & Chemistry Tutor', 'price': 45000, 'exp': '8 Years'},
            {'name': 'Ms. Grace Kemigisha', 'title': 'Primary Science Specialist', 'price': 30000, 'exp': '5 Years'},
        ]
        
        coaches = []
        for data in coach_data:
            username = data['name'].replace(' ', '').replace('.', '').lower()
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com', 'role': 'TEACHER', 'is_coach': True, 'first_name': data['name'].split()[0], 'last_name': data['name'].split()[-1]}
            )
            if created:
                user.set_password('password123')
                user.save()
            
            coach, _ = Coach.objects.get_or_create(
                user=user,
                defaults={
                    'title': data['title'],
                    'price_per_hour': data['price'],
                    'experience': data['exp'],
                    'description': f"Expert tutoring by {data['name']} with {data['exp']} of experience."
                }
            )
            coaches.append(coach)
            
        self.stdout.write(self.style.SUCCESS(f'Verified {len(coaches)} coaches and {len(students)} students.'))

        # 3. Generate Availability for Coaches
        self.stdout.write('Generating availability schedules...')
        for coach in coaches:
            # Monday to Friday (1-5)
            for day in range(1, 6):
                # Morning Block
                CoachAvailabilityRange.objects.create(
                    coach=coach, day_of_week=day,
                    start_time=time(9, 0), end_time=time(12, 0), is_active=True
                )
                # Afternoon Block
                CoachAvailabilityRange.objects.create(
                    coach=coach, day_of_week=day,
                    start_time=time(14, 0), end_time=time(17, 0), is_active=True
                )
            # Saturday (6) - Morning only
            CoachAvailabilityRange.objects.create(
                coach=coach, day_of_week=6,
                start_time=time(10, 0), end_time=time(13, 0), is_active=True
            )
            # Sunday (0) - Inactive (explicitly left out or created as inactive)
            CoachAvailabilityRange.objects.create(
                coach=coach, day_of_week=0,
                start_time=time(0, 0), end_time=time(0, 0), is_active=False
            )

        # 4. Generate some Booking Sessions
        self.stdout.write('Generating sample bookings...')
        today = datetime.now().date()
        statuses = ['pending', 'confirmed', 'completed']
        
        for _ in range(15): # Create 15 random bookings
            coach = random.choice(coaches)
            student = random.choice(students)
            
            # Pick a random date within the next 14 days (excluding Sunday)
            days_ahead = random.randint(1, 14)
            booking_date = today + timedelta(days=days_ahead)
            if booking_date.weekday() == 6: # If Sunday (weekday()=6 in python, our array logic uses 0=Sun), shift to Mon
                booking_date += timedelta(days=1)
                
            # Pick a regular slot (e.g. 10:00 AM or 14:00 PM)
            start_hour = random.choice([9, 10, 14, 15])
            duration = random.choice([1, 2])
            
            start_time = time(start_hour, 0)
            end_time = time(start_hour + duration, 0)
            
            status = random.choice(statuses)
            
            # Simple conflict avoidance for the script - only create if exact slot is free
            conflict = CoachingSession.objects.filter(
                coach=coach, date=booking_date, start_time=start_time
            ).exists()
            
            if not conflict:
                session = CoachingSession(
                    coach=coach,
                    student=student,
                    date=booking_date,
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    status=status,
                    total_price=coach.price_per_hour * duration,
                    note=f"Sample booking generated by script for {student.username}."
                )
                # Avoid signal execution matching verify_slots.py
                session.save()
                
                if status == 'confirmed':
                    session.meeting_link = f"https://meet.google.com/{random.choice(['abc-xyz-123', 'def-uvw-456', 'hij-rst-789'])}"
                    session.save()

        session_count = CoachingSession.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {session_count} sample bookings.'))
        self.stdout.write(self.style.SUCCESS('Data load complete!'))
