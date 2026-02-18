import os
import django
import random
from datetime import datetime, timedelta, time
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from educoach.models import Coach, CoachingSession, VirtualClass, ClassEnrollment
from users.models import Profile

User = get_user_model()

def create_coach_user(username, email, first_name, last_name, bio, role='TEACHER'):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': role
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        print(f"Created user: {username}")
    
    # Ensure profile exists (signal should create it, but just in case)
    Profile.objects.get_or_create(user=user, defaults={'bio': bio})
    return user

def create_student_user(username, email, first_name, last_name):
    return create_coach_user(username, email, first_name, last_name, "I am a student eager to learn.", role='STUDENT')

def populate():
    print("Populating EduCoach data...")

    # 1. Create Coaches
    coaches_data = [
        {
            "username": "dr_sarah",
            "email": "sarah@edumerc.com",
            "first_name": "Sarah",
            "last_name": "Nabirye",
            "title": "Senior P.7 Science Expert",
            "experience": "12 Years",
            "price": 45000,
            "desc": "Focused on PLE preparation with high success rates.",
            "subjects": ["Science", "Mathematics"],
            "levels": ["P.6", "P.7"],
            "badges": ["Top Rated", "UNEB Examiner"]
        },
        {
            "username": "mr_john",
            "email": "john@edumerc.com",
            "first_name": "John",
            "last_name": "Okello",
            "title": "Math Wizard & Calculus Tutor",
            "experience": "8 Years",
            "price": 50000,
            "desc": "Making math easy and fun for everyone.",
            "subjects": ["Mathematics", "Physics"],
            "levels": ["S.4", "S.6"],
            "badges": ["Math Whiz"]
        },
        {
            "username": "tr_mary",
            "email": "mary@edumerc.com",
            "first_name": "Mary",
            "last_name": "Kato",
            "title": "English Literature Specialist",
            "experience": "15 Years",
            "price": 40000,
            "desc": "Helping students master English and Literature.",
            "subjects": ["English", "Literature"],
            "levels": ["S.3", "S.4"],
            "badges": ["Literature Lover", "Best Teacher 2024"]
        }
    ]

    coaches = []
    for data in coaches_data:
        user = create_coach_user(data['username'], data['email'], data['first_name'], data['last_name'], data['desc'])
        
        coach, created = Coach.objects.get_or_create(
            user=user,
            defaults={
                'title': data['title'],
                'experience': data['experience'],
                'price_per_hour': data['price'],
                'description': data['desc'],
                'subjects': data['subjects'],
                'levels': data['levels'],
                'badges': data['badges'],
                'rating': round(random.uniform(4.0, 5.0), 1),
                'review_count': random.randint(10, 200)
            }
        )
        if created:
            print(f"Created coach profile for {user.username}")
        coaches.append(coach)

    # 2. Create Students
    students_data = [
        ("student_tom", "tom@school.com", "Tom", "Mayanja"),
        ("student_jane", "jane@school.com", "Jane", "Akelo"),
        ("student_peter", "peter@school.com", "Peter", "Kintu"),
    ]
    
    students = []
    for u, e, f, l in students_data:
        students.append(create_student_user(u, e, f, l))

    # 3. Create Virtual Classes
    class_titles = [
        "Mastering Primary Science: The PLE Intensive",
        "Calculus made Simple: Limits and Derivatives",
        "Othello: In-depth Analysis",
        "P.7 Math Revision Marathon"
    ]

    for i, title in enumerate(class_titles):
        coach = random.choice(coaches)
        v_class, created = VirtualClass.objects.get_or_create(
            title=title,
            coach=coach,
            defaults={
                'subject': coach.subjects[0],
                'level': coach.levels[0],
                'start_date': (timezone.now() + timedelta(days=random.randint(5, 30))).date(),
                'schedule': f"Every {random.choice(['Monday', 'Tuesday', 'Wednesday'])} 4:00 PM",
                'duration_weeks': random.randint(4, 12),
                'price': float(coach.price_per_hour) * 4, # approximated batch price
                'capacity': 50,
                'description': f"Join {coach.user.first_name} for an intensive course on {title}."
            }
        )
        if created:
            print(f"Created class '{title}' by {coach.user.username}")
            
            # Enroll some students
            for student in random.sample(students, k=random.randint(1, len(students))):
                ClassEnrollment.objects.get_or_create(
                    virtual_class=v_class,
                    student=student,
                    defaults={'payment_reference': f"REF-{random.randint(1000,9999)}"}
                )
                print(f"  Enrolled {student.username}")

    # 4. Create Booking Sessions
    for student in students:
        for _ in range(random.randint(1, 3)):
            coach = random.choice(coaches)
            date = (timezone.now() + timedelta(days=random.randint(1, 14))).date()
            time_obj = time(random.randint(9, 17), 0) # 9 AM to 5 PM
            
            session, created = CoachingSession.objects.get_or_create(
                coach=coach,
                student=student,
                date=date,
                time=time_obj,
                defaults={
                    'duration': 1,
                    'note': "I need help with revision.",
                    'status': random.choice(['pending', 'confirmed', 'completed']),
                    'total_price': coach.price_per_hour
                }
            )
            if session.status == 'confirmed':
                session.meeting_link = "https://meet.google.com/abc-defg-hij"
                session.save()
            
            if created:
                print(f"Created session: {student.username} with {coach.user.username}")

    print("Done populating EduCoach!")

if __name__ == '__main__':
    populate()
