import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from edupedia.models import School, SchoolEvent, SchoolReview, SchoolGalleryImage, SchoolAdministrator
from educlubs.models import Club, ClubCategory, Topic, Lesson, RoleModel
from edushop.models import Category, Product, Bundle
from edufundme.models import Scholarship, Campaign
from eduquest.models import Material, MaterialOrder
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
        detailed_schools = [
            {
                'name': 'Heritage International School',
                'motto': 'Excellence in Every Child',
                'location': 'Lubowa, Entebbe Road',
                'description': 'A premium international school offering the British curriculum with state-of-the-art facilities and a global outlook.',
                'email': 'admissions@heritage.ac.ug',
                'website': 'https://heritage.ac.ug'
            },
            {
                'name': 'St. Mary\'s High School',
                'motto': 'Virtue and Labor',
                'location': 'Kitende, Kampala',
                'description': 'One of the leading traditional schools in Uganda, known for academic excellence and discipline.',
                'email': 'info@stmarys.edu',
                'website': 'https://stmaryskitende.com'
            },
            {
                'name': 'Hillside Primary School',
                'motto': 'Aim Higher',
                'location': 'Naalya, Kampala',
                'description': 'A top-tier primary school dedicated to nurturing young minds through a holistic approach to education.',
                'email': 'hillside@education.ug',
                'website': 'https://hillside.ac.ug'
            },
            {
                'name': 'Victoria Lake College',
                'motto': 'Leading with Purpose',
                'location': 'Jinja, Source of the Nile',
                'description': 'A scenic boarding school focused on leadership, environmental studies, and aquatic sports.',
                'email': 'info@victorialake.com',
                'website': 'https://victorialake.com'
            },
            {
                'name': 'Nile Valley Technical School',
                'motto': 'Skills for Life',
                'location': 'Nakawa, Kampala',
                'description': 'Specializing in vocational and technical skills, from robotics to sustainable construction.',
                'email': 'nakatech@gov.ug',
                'website': 'https://niletech.ac.ug'
            },
            {
                'name': 'Rwenzori Mountains Academy',
                'motto': 'Heights of Knowledge',
                'location': 'Kasese, Rwenzori Ridge',
                'description': 'An eco-friendly science academy situated at the foothills of the Rwenzori mountains.',
                'email': 'rwenzori@science.ac.ug',
                'website': 'https://rwenzori.ac.ug'
            },
            {
                'name': 'Crested Crane High School',
                'motto': 'Integrity and Honor',
                'location': 'Gulu, Northern Region',
                'description': 'A modern high school known for sports excellence and community leadership programs.',
                'email': 'crested@high.ug',
                'website': 'https://crestedcrane.com'
            },
            {
                'name': 'Mount Elgon Prep',
                'motto': 'The First Step',
                'location': 'Mbale, Eastern Uganda',
                'description': 'A nurturing environment for early childhood and primary education with a focus on arts and music.',
                'email': 'admin@mtelgon.ac.ug',
                'website': 'https://mtelgon.ac.ug'
            }
        ]

        schools = []
        for s_data in detailed_schools:
            s_slug = slugify(s_data['name'])
            school, created = School.objects.get_or_create(
                name=s_data['name'],
                slug=s_slug,
                defaults={
                    'motto': s_data['motto'],
                    'location': s_data['location'],
                    'description': s_data['description'],
                    'email': s_data['email'],
                    'website': s_data['website'],
                    'logo': 'school_logos/master_logo.png',
                    'cover_image': 'school_covers/master_cover.jpg'
                }
            )
            schools.append(school)
            if created:
                # Add Gallery
                SchoolGalleryImage.objects.create(school=school, image='school_gallery/master_gallery.jpg', caption='Main Campus Overview')
                
                # Add Administrator
                SchoolAdministrator.objects.create(
                    school=school, 
                    name=f'Dr. {s_data["name"].split()[0]} Principal',
                    role='Headteacher',
                    bio='A veteran educator with over 20 years of experience in institutional management.'
                )
                
                # Add Event
                SchoolEvent.objects.create(
                    school=school, 
                    title='Annual Science Fair', 
                    description='A showcase of student innovation and technological projects.', 
                    date=date.today() + timedelta(days=random.randint(10, 60))
                )
                
                # Add Review
                SchoolReview.objects.create(
                    school=school, 
                    user=student_user, 
                    rating=random.randint(4, 5), 
                    comment=f'I love studying at {school.name}. The environment is very supportive.'
                )

        # 3. Club Categories and Clubs
        self.stdout.write('Creating clubs...')
        tech_cat, _ = ClubCategory.objects.get_or_create(name='Technology', slug='technology')
        arts_cat, _ = ClubCategory.objects.get_or_create(name='Arts & Culture', slug='arts-culture')
        science_cat, _ = ClubCategory.objects.get_or_create(name='Science & Innovation', slug='science-innovation')

        # Robotics
        robotics_club, created = Club.objects.get_or_create(
            name='Robotics & AI',
            defaults={'category': tech_cat, 'description': 'Learn to build the future.'}
        )
        if created:
            topic = Topic.objects.create(club=robotics_club, title='Introduction to Arduino', order=1)
            Lesson.objects.create(topic=topic, title='Hello World: Blinking LED', text_content='Your first circuit.', order=1)
            RoleModel.objects.create(club=robotics_club, name='Elon Musk', bio='Visionary Engineer', contribution='Space & AI')

        # Drama Club
        drama_club, created = Club.objects.get_or_create(
            name='Drama & Performing Arts',
            defaults={'category': arts_cat, 'description': 'Express yourself on stage.'}
        )
        if created:
            topic = Topic.objects.create(club=drama_club, title='Stage Presence', order=1)
            Lesson.objects.create(topic=topic, title='Body Language Basics', text_content='Mastering the stage.', order=1)
            RoleModel.objects.create(club=drama_club, name='Viola Davis', bio='Academy Award Winner', contribution='Acting')

        # Science Club
        science_club, created = Club.objects.get_or_create(
            name='Young Scientists',
            defaults={'category': science_cat, 'description': 'Exploring the natural world.'}
        )
        if created:
            topic = Topic.objects.create(club=science_club, title='Renewable Energy', order=1)
            Lesson.objects.create(topic=topic, title='Solar Power Experiments', text_content='Harnessing the sun.', order=1)
            RoleModel.objects.create(club=science_club, name='Katherine Johnson', bio='NASA Mathematician', contribution='Physics & Math')
        
        self.stdout.write('Clubs seeded.')

        # 4. Shop Categories and Products
        self.stdout.write('Creating shop items...')
        stationery, _ = Category.objects.get_or_create(name='Stationery', slug='stationery')
        books, _ = Category.objects.get_or_create(name='Textbooks', slug='textbooks')
        uniforms, _ = Category.objects.get_or_create(name='Uniforms', slug='uniforms')
        electronics, _ = Category.objects.get_or_create(name='Electronics', slug='electronics')
        
        notebook, _ = Product.objects.get_or_create(
            title='Edumerk Branded Notebook',
            defaults={'category': stationery, 'price': 5.00, 'stock': 100}
        )
        bio_book, _ = Product.objects.get_or_create(
            title='Advanced Biology Vol 1',
            defaults={'category': books, 'price': 25.00, 'stock': 50}
        )
        calculator, _ = Product.objects.get_or_create(
            title='Scientific Calculator FX-991EX',
            defaults={'category': electronics, 'price': 45.00, 'stock': 30}
        )
        uniform_set, _ = Product.objects.get_or_create(
            title='Full School Uniform Set',
            defaults={'category': uniforms, 'price': 60.00, 'stock': 200, 'description': 'Complete set for secondary level.'}
        )
        
        bundle1, created = Bundle.objects.get_or_create(
            title='Science Starter Pack',
            defaults={'price': 28.00, 'description': 'Essential kit for young scientists.'}
        )
        if created: bundle1.products.add(notebook, bio_book)

        bundle2, created = Bundle.objects.get_or_create(
            title='Tech Savvy Student Pack',
            defaults={'price': 48.00, 'description': 'Stay ahead with tech tools.'}
        )
        if created: bundle2.products.add(notebook, calculator)

        self.stdout.write('Shop items seeded.')

        # 5. Fund Me
        self.stdout.write('Creating fundme data...')
        Scholarship.objects.get_or_create(
            title='STEM Excellence Scholarship',
            provider='Tech Foundation',
            amount=1000.00,
            deadline=date.today() + timedelta(days=60),
            eligibility='Students interested in STEM with 3.5+ GPA'
        )
        Scholarship.objects.get_or_create(
            title='Artistic Vision Award',
            provider='Creativity Hub',
            amount=500.00,
            deadline=date.today() + timedelta(days=45),
            eligibility='Outstanding performance in digital or traditional arts.'
        )

        Campaign.objects.get_or_create(
            title='Library Renovation for Heritage Intl',
            target_amount=5000.00,
            school=schools[0],
            description='Help us modernize our learning resource center.'
        )
        Campaign.objects.get_or_create(
            title='Solar Power for St. Mary High',
            target_amount=3500.00,
            school=schools[1],
            description='Sustainable energy for a sustainable future.'
        )

        # 6. EduQuest
        self.stdout.write('Creating eduquest data...')
        math_eot, created = Material.objects.get_or_create(
            title='S.1 Mathematics EOT Exam 2024',
            defaults={
                'material_type': 'EXAM',
                'session': 'EOT',
                'description': 'End of Term 3 exam paper.',
                'price': 2.50
            }
        )
        phys_mid, _ = Material.objects.get_or_create(
            title='S.4 Physics MID Term Paper 2024',
            defaults={
                'material_type': 'EXAM',
                'session': 'MID',
                'description': 'Focused on mechanics and electricity.',
                'price': 3.00
            }
        )
        hist_notes, _ = Material.objects.get_or_create(
            title='History of East Africa - Full Notes',
            defaults={
                'material_type': 'OTHER',
                'description': 'Comprehensive notes for O-Level.',
                'price': 10.00
            }
        )

        MaterialOrder.objects.get_or_create(
            user=student_user,
            material=math_eot,
            defaults={'status': 'COMPLETED'}
        )
        MaterialOrder.objects.get_or_create(
            user=student_user,
            material=hist_notes,
            defaults={'status': 'PENDING'}
        )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
