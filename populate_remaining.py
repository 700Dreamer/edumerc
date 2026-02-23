import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.text import slugify

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from edufundme.models import Scholarship, Application, Campaign
from eduquest.models import Material, MaterialOrder
from edupedia.models import School

User = get_user_model()

def populate_remaining():
    print("Populating EduFundMe and EduQuest...")

    # 1. EduFundMe - Scholarships
    scholarships_data = [
        {
            "title": "STEM Excellence Scholarship 2026",
            "description": "A prestigious scholarship for students excelling in Science, Technology, Engineering, and Mathematics.",
            "provider": "EduMerk Foundation",
            "amount": 1000000,
            "deadline": (timezone.now() + timedelta(days=60)).date(),
            "eligibility": "Minimum 80% in Science subjects."
        },
        {
            "title": "Community Leaders Grant",
            "description": "Supporting students who show exceptional leadership in their local communities.",
            "provider": "Uganda Youth Alliance",
            "amount": 500000,
            "deadline": (timezone.now() + timedelta(days=45)).date(),
            "eligibility": "Open to all secondary school students."
        }
    ]

    for data in scholarships_data:
        Scholarship.objects.get_or_create(title=data['title'], defaults=data)
        print(f"  Scholarship: {data['title']}")

    # 2. EduFundMe - Campaigns
    schools = School.objects.all()
    if schools.exists():
        campaigns_data = [
            {
                "title": "Digital Literacy Lab Fund",
                "description": "Raising funds to equip our new computer lab with 20 modern laptops.",
                "target_amount": 5000000,
                "school": random.choice(schools)
            },
            {
                "title": "School Library Expansion",
                "description": "Help us buy 500 new textbooks and renovate our library space.",
                "target_amount": 2000000,
                "school": random.choice(schools)
            }
        ]
        for data in campaigns_data:
            Campaign.objects.get_or_create(title=data['title'], defaults=data)
            print(f"  Campaign: {data['title']} for {data['school'].name}")

    # 3. EduQuest - Materials
    materials_data = [
        {
            "title": "P.7 Mathematics Mock Paper 2024",
            "material_type": "EXAM",
            "session": "MID",
            "description": "Comprehensive mock exam with marking guide.",
            "price": 5000
        },
        {
            "title": "S.4 Physics Past Papers (2018-2023)",
            "material_type": "PAST_PAPER",
            "session": "NONE",
            "description": "Collection of past papers with detailed solutions.",
            "price": 10000
        },
        {
            "title": "Primary Science Detailed Revision Notes",
            "material_type": "OTHER",
            "session": "NONE",
            "description": "Level P.5 - P.7 topics explained simply.",
            "price": 7500
        }
    ]

    materials = []
    for data in materials_data:
        m, created = Material.objects.get_or_create(title=data['title'], defaults=data)
        materials.append(m)
        print(f"  Material: {data['title']}")

    # 4. EduQuest - Material Orders
    students = User.objects.filter(role='STUDENT')
    if students.exists() and materials:
        for _ in range(5):
            student = random.choice(students)
            material = random.choice(materials)
            MaterialOrder.objects.create(
                user=student,
                material=material,
                status=random.choice(['PENDING', 'APPROVED', 'PAID']),
                session=random.choice(['BOT', 'MID', 'EOT']),
                school_name=f"{student.username.capitalize()} International School",
                phone="+256 700 000 000",
                estimated_amount=material.price
            )
            print(f"  Order created for {student.username}")

    print("Done populating remaining modules!")

if __name__ == '__main__':
    populate_remaining()
