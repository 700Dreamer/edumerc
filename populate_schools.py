import os
import django
from django.utils.text import slugify
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from edupedia.models import School, SchoolEvent, SchoolAdministrator, PromotionalMaterial

def populate_schools():
    # 1. Kampala Parents School (Primary)
    kps_name = "Kampala Parents School"
    kps, created = School.objects.get_or_create(
        slug=slugify(kps_name),
        defaults={
            'name': kps_name,
            'location': 'Naguru, Kampala',
            'motto': 'We Struggle for the Future',
            'description': 'A leading primary school in Kampala providing quality education.',
            'email': 'info@kampalaparents.com',
            'phone': '+256 123 456 789',
            'website': 'https://kampalaparents.com',
            'video_360_url': 'https://youtube.com/watch?v=sample360',
        }
    )
    print(f"School: {kps.name}")

    SchoolEvent.objects.get_or_create(
        school=kps,
        title="Sports Day 2026",
        defaults={
            'description': 'Annual sports gala.',
            'date': datetime.now() + timedelta(days=30)
        }
    )

    SchoolAdministrator.objects.get_or_create(
        school=kps,
        name="Mrs. Principal",
        defaults={'role': 'Headteacher', 'bio': 'Experienced educator with 20+ years.'}
    )

    # 2. Gayaza High School (Secondary)
    ghs_name = "Gayaza High School"
    ghs, created = School.objects.get_or_create(
        slug=slugify(ghs_name),
        defaults={
            'name': ghs_name,
            'location': 'Gayaza, Wakiso',
            'motto': 'Never Give Up',
            'description': 'The oldest girls boarding school in Uganda.',
            'email': 'admin@gayaza.sc.ug',
            'phone': '+256 987 654 321',
            'website': 'https://gayazalhs.sc.ug',
        }
    )
    print(f"School: {ghs.name}")

    PromotionalMaterial.objects.get_or_create(
        school=ghs,
        title="2026 Prospectus",
        defaults={'material_type': 'Prospectus', 'file': 'sample_prospectus.pdf'}
    )

    # 3. Uganda Martyrs SS Namugongo
    nam_name = "Uganda Martyrs SS Namugongo"
    nam, created = School.objects.get_or_create(
        slug=slugify(nam_name),
        defaults={
            'name': nam_name,
            'location': 'Namugongo, Wakiso',
            'motto': 'Perseverance and Success',
            'description': 'Excellence in both sciences and arts.',
        }
    )
    print(f"School: {nam.name}")

if __name__ == '__main__':
    print("Populating Edupedia schools...")
    populate_schools()
    print("Done!")
