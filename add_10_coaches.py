import os
import django
import random
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from educoach.models import Coach
from users.models import Profile

User = get_user_model()

def create_coach_user(username, email, first_name, last_name, bio, role='TEACHER'):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': role,
            'is_coach': True
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        print(f"Created user: {username}")
    
    Profile.objects.get_or_create(user=user, defaults={'bio': bio})
    return user

def add_coaches():
    print("Adding 10 more coaches...")
    coaches_data = [
        {
            "username": "moses_m", "email": "moses@edumerc.com", "first_name": "Moses", "last_name": "Musoke",
            "title": "A-Level Physics & Math Specialist", "experience": "10 Years", "price": 55000,
            "desc": "Focusing on complex mechanics and calculus.", "subjects": ["Physics", "Mathematics"],
            "levels": ["S.5", "S.6"], "badges": ["Top Rated", "Math Guru"]
        },
        {
            "username": "ritah_n", "email": "ritah@edumerc.com", "first_name": "Ritah", "last_name": "Namatovu",
            "title": "Biology & Chemistry Expert", "experience": "7 Years", "price": 48000,
            "desc": "Passionate about lab experiments and organic chemistry.", "subjects": ["Biology", "Chemistry"],
            "levels": ["S.3", "S.4"], "badges": ["Science Whiz"]
        },
        {
            "username": "peter_k", "email": "peter@edumerc.com", "first_name": "Peter", "last_name": "Kizito",
            "title": "ICT & Computer Studies Instructor", "experience": "5 Years", "price": 45000,
            "desc": "Empowering students with digital skills and coding.", "subjects": ["ICT", "Computer Studies"],
            "levels": ["S.1", "S.6", "Tertiary"], "badges": ["Tech Expert"]
        },
        {
            "username": "grace_a", "email": "grace@edumerc.com", "first_name": "Grace", "last_name": "Akello",
            "title": "Primary English & Literature Tutor", "experience": "9 Years", "price": 42000,
            "desc": "Specializing in creative writing and comprehension.", "subjects": ["English", "Literature"],
            "levels": ["P.5", "P.6", "P.7"], "badges": ["Best Tutor 2025"]
        },
        {
            "username": "david_o", "email": "david@edumerc.com", "first_name": "David", "last_name": "Okello",
            "title": "Economics & Entrepreneurship Coach", "experience": "11 Years", "price": 60000,
            "desc": "Preparing future entrepreneurs and economists.", "subjects": ["Economics", "Entrepreneurship"],
            "levels": ["S.5", "S.6"], "badges": ["Business Strategist"]
        },
        {
            "username": "agnes_n", "email": "agnes@edumerc.com", "first_name": "Agnes", "last_name": "Nabirye",
            "title": "Geography & History Specialist", "experience": "6 Years", "price": 40000,
            "desc": "Exploring the world through maps and stories.", "subjects": ["Geography", "History"],
            "levels": ["S.1", "S.2", "S.3", "S.4"], "badges": ["Eco Warrior"]
        },
        {
            "username": "james_t", "email": "james@edumerc.com", "first_name": "James", "last_name": "Tumusiime",
            "title": "Religious Education Expert", "experience": "14 Years", "price": 35000,
            "desc": "Deepening understanding of faith and ethics.", "subjects": ["Religious Education", "CRE"],
            "levels": ["P.1", "P.7"], "badges": ["Ethical Mentor"]
        },
        {
            "username": "sarah_atim", "email": "sarah_a@edumerc.com", "first_name": "Sarah", "last_name": "Atim",
            "title": "Fine Art & Music Teacher", "experience": "8 Years", "price": 40000,
            "desc": "Unlocking creativity through art and sound.", "subjects": ["Fine Art", "Music"],
            "levels": ["General"], "badges": ["Artist Extraordinaire"]
        },
        {
            "username": "joseph_l", "email": "joseph@edumerc.com", "first_name": "Joseph", "last_name": "Lule",
            "title": "Physical Education & Sports Coach", "experience": "4 Years", "price": 30000,
            "desc": "Promoting fitness and team spirit.", "subjects": ["Physical Education", "Sports"],
            "levels": ["General"], "badges": ["Fitness King"]
        },
        {
            "username": "juliet_n", "email": "juliet@edumerc.com", "first_name": "Juliet", "last_name": "Nakafeero",
            "title": "Luganda & Culture Specialist", "experience": "15 Years", "price": 38000,
            "desc": "Teaching the rich heritage of Luganda.", "subjects": ["Luganda", "Culture"],
            "levels": ["P.1", "S.4"], "badges": ["Cultural Ambassador"]
        }
    ]

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
                'rating': round(random.uniform(4.2, 5.0), 1),
                'review_count': random.randint(20, 150)
            }
        )
        if created:
            print(f"Created coach profile for {user.username}")
        else:
            print(f"Coach profile already exists for {user.username}")

    print("Finished adding 10 coaches.")

if __name__ == '__main__':
    add_coaches()
