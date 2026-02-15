import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import MainCategory, SubCategory, Club

def seed():
    # Clear existing
    MainCategory.objects.all().delete()
    SubCategory.objects.all().delete()
    Club.objects.all().delete()
    
    # 1. Main Categories
    subject = MainCategory.objects.create(name="Subject Clubs", slug="subject-clubs")
    social = MainCategory.objects.create(name="Social Clubs", slug="social-clubs")
    teachers = MainCategory.objects.create(name="Teacher Hubs", slug="teacher-hubs")
    
    # 2. Sub-categories for Subject
    levels = ["Nursery", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "S1", "S2", "S3", "S4", "S5", "S6"]
    for i, level in enumerate(levels):
        SubCategory.objects.create(main_category=subject, name=level, slug=level.lower(), order=i)

    # 3. Sub-categories for Social
    SubCategory.objects.create(main_category=social, name="Sports", slug="sports", order=0)
    SubCategory.objects.create(main_category=social, name="Business", slug="business", order=1)
    SubCategory.objects.create(main_category=social, name="Religious Clubs", slug="religious", order=2)

    # 4. Sub-categories for Teachers
    SubCategory.objects.create(main_category=teachers, name="Administrative", slug="administrative", order=0)
    SubCategory.objects.create(main_category=teachers, name="Professional Hub", slug="professional", order=1)

    # 5. Realistic Clubs for P7
    p7 = SubCategory.objects.get(name="P7", main_category=subject)
    Club.objects.create(name="Math Club", subcategory=p7, description="Advanced calculations and PLE prep.")
    Club.objects.create(name="English Club", subcategory=p7, description="Grammar, debate and literature.")
    Club.objects.create(name="Science Club", subcategory=p7, description="Experiments and natural wonders.")
    Club.objects.create(name="Social Studies Club", subcategory=p7, description="History and geography mastery.")

    print("Final seed complete!")

if __name__ == "__main__":
    seed()
