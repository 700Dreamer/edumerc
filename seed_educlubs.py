import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import (
    MainCategory, SubjectLevel, SubjectClub, Topic, Lesson,
    SocialGroup, SocialClub, TeacherCategory, TeacherClub
)

def seed_educlubs():
    print("Seeding heterogeneous Educlubs...")
    
    # 1. Main Categories
    subject_cat, _ = MainCategory.objects.get_or_create(name="Subject Clubs", slug="subject-clubs")
    social_cat, _ = MainCategory.objects.get_or_create(name="Social Clubs", slug="social-clubs")
    teacher_cat, _ = MainCategory.objects.get_or_create(name="Teacher Hubs", slug="teacher-hubs")
    
    # --- SUBJECT BRANCH ---
    levels = [
        "Nursery", "Pre-Primary", "P1", "P2", "P3", "P4", "P5", "P6", "P7",
        "S1", "S2", "S3", "S4", "S5", "S6"
    ]
    for i, level_name in enumerate(levels):
        lvl, _ = SubjectLevel.objects.get_or_create(
            main_category=subject_cat,
            name=level_name,
            slug=level_name.lower().replace(" ", "-"),
            order=i
        )
        if level_name == "P7":
            # Add some clubs
            math, _ = SubjectClub.objects.get_or_create(
                level=lvl,
                name="Math Club",
                description="Mastering primary mathematics."
            )
            eng, _ = SubjectClub.objects.get_or_create(
                level=lvl,
                name="English Club",
                description="Grammar and literature excellence."
            )
            
            # Add Topic/Lesson to Math
            t1, _ = Topic.objects.get_or_create(club=math, title="Fractions", order=1)
            Lesson.objects.get_or_create(topic=t1, title="Introduction to Fractions", order=1)
            
    # --- SOCIAL BRANCH ---
    sports, _ = SocialGroup.objects.get_or_create(
        main_category=social_cat,
        name="Sports",
        slug="sports",
        icon="sports_soccer"
    )
    biz, _ = SocialGroup.objects.get_or_create(
        main_category=social_cat,
        name="Business",
        slug="business",
        icon="business"
    )
    
    SocialClub.objects.get_or_create(
        group=sports,
        name="Football Club",
        description="Daily training and matches.",
        facilitator="Coach Kizito"
    )
    SocialClub.objects.get_or_create(
        group=biz,
        name="Entrepreneurs Club",
        description="Learning small business skills.",
        facilitator="Ms. Namubiru"
    )
    
    # --- TEACHER BRANCH ---
    admin_cat, _ = TeacherCategory.objects.get_or_create(
        main_category=teacher_cat,
        name="Administrative",
        slug="administrative",
        is_administrative=True
    )
    prof_cat, _ = TeacherCategory.objects.get_or_create(
        main_category=teacher_cat,
        name="Professional Hub",
        slug="professional-hub"
    )
    
    TeacherClub.objects.get_or_create(
        category=admin_cat,
        name="Headteachers Forum",
        description="Policy discussion and school management.",
        duration="Continuous"
    )
    
    print("Seeding complete!")

if __name__ == "__main__":
    seed_educlubs()
