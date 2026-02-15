import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from edupedia.models import School, SchoolEvent, SchoolReview
from educlubs.models import Club, ClubCategory, Topic, Lesson, RoleModel
from edushop.models import Category, Product, Bundle
from edufundme.models import Scholarship, Campaign
from django.utils.text import slugify
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data for Edumerk'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Users
        self.stdout.write('Creating users...')
        admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@edumerk.com', 'role': 'ADMIN'})
        if created:
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write('Admin user created.')

        student_user, created = User.objects.get_or_create(username='student1', defaults={'email': 'student1@example.com', 'role': 'STUDENT'})
        if created:
            student_user.set_password('pass123')
            student_user.save()
            self.stdout.write('Student user created.')

        teacher_user, created = User.objects.get_or_create(username='teacher1', defaults={'email': 'teacher1@example.com', 'role': 'TEACHER'})
        if created:
            teacher_user.set_password('pass123')
            teacher_user.save()
            self.stdout.write('Teacher user created.')

        # 2. Schools
        self.stdout.write('Creating schools...')
        school_names = ['St. Mary Academy', 'Green Hill Primary', 'Nakawa Technical Institute']
        schools = []
        for name in school_names:
            school, created = School.objects.get_or_create(
                name=name,
                slug=slugify(name),
                location='Kampala, Uganda',
                description=f'Leading educational institution: {name}'
            )
            schools.append(school)
            if created:
                SchoolEvent.objects.create(school=school, title='Annual Sports Day', description='Compete for the gold!', date=date.today() + timedelta(days=30))
                SchoolReview.objects.create(school=school, user=student_user, rating=5, comment='Amazing school with great facilities.')

        # 3. Club Categories and Clubs
        self.stdout.write('Creating clubs...')
        coding_cat, _ = ClubCategory.objects.get_or_create(name='Technology', slug='technology')
        robotics_club, created = Club.objects.get_or_create(
            name='Robotics & AI',
            defaults={
                'category': coding_cat,
                'description': 'Learn to build the future.'
            }
        )
        if created:
            topic = Topic.objects.create(club=robotics_club, title='Introduction to Arduino', order=1)
            Lesson.objects.create(topic=topic, title='Hello World: Blinking LED', text_content='Your first circuit.', order=1)
            RoleModel.objects.create(club=robotics_club, name='Elon Musk', bio='Visionary Engineer', expertise='Space & AI')
            self.stdout.write('Club created.')

        # 4. Shop Categories and Products
        self.stdout.write('Creating shop items...')
        stationery, _ = Category.objects.get_or_create(name='Stationery', slug='stationery')
        books, _ = Category.objects.get_or_create(name='Textbooks', slug='textbooks')
        
        notebook, created = Product.objects.get_or_create(
            title='Edumerk Branded Notebook',
            defaults={
                'category': stationery,
                'price': 5.00,
                'stock': 100
            }
        )
        bio_book, created = Product.objects.get_or_create(
            title='Advanced Biology Vol 1',
            defaults={
                'category': books,
                'price': 25.00,
                'stock': 50
            }
        )
        
        bundle, created = Bundle.objects.get_or_create(
            title='Science Starter Pack',
            defaults={
                'price': 28.00,
                'description': 'Essential kit for young scientists.'
            }
        )
        if created:
            bundle.products.add(notebook, bio_book)
            self.stdout.write('Bundle created.')

        # 5. Fund Me
        self.stdout.write('Creating fundme data...')
        Scholarship.objects.get_or_create(
            title='STEM Excellence Scholarship',
            provider='Tech Foundation',
            amount=1000.00,
            deadline=date.today() + timedelta(days=60),
            eligibility='Students interested in STEM with 3.5+ GPA'
        )
        Campaign.objects.get_or_create(
            title='Library Renovation for St. Mary',
            target_amount=5000.00,
            school=schools[0],
            description='Help us modernize our learning resource center.'
        )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
