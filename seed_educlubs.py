import os
import django
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import (
    MainCategory, SubjectLevel, SubjectClub, Topic, Lesson,
    SocialGroup, SocialClub, ClubDiscussion,
    TeacherCategory, TeacherClub, RoleModel, PracticalApplication
)
from django.contrib.auth import get_user_model

User = get_user_model()

def seed_educlubs():
    print("Seeding heterogeneous Educlubs...")
    
    # 1. Main Categories
    subject_cat, _ = MainCategory.objects.get_or_create(name="Subject Clubs", slug="subject-clubs")
    social_cat, _ = MainCategory.objects.get_or_create(name="Social Clubs", slug="social-clubs")
    teacher_cat, _ = MainCategory.objects.get_or_create(name="Teacher Hubs", slug="teacher-hubs")

    # 2. Subject Branch
    p1, _ = SubjectLevel.objects.get_or_create(main_category=subject_cat, name="P1", order=1)
    p7, _ = SubjectLevel.objects.get_or_create(main_category=subject_cat, name="P7", order=7)

    math, _ = SubjectClub.objects.get_or_create(
        level=p7, 
        name="Math Club", 
        description="Mastering primary mathematics.",
        icon="📚"
    )
    
    # Topics for Subject
    t1, _ = Topic.objects.get_or_create(subject_club=math, title="Fractions", order=1)
    Lesson.objects.get_or_create(topic=t1, title="Intro to Fractions", content_type="Video Lesson")
    Lesson.objects.get_or_create(topic=t1, title="Adding Fractions", content_type="Reading Material")

    # Role Model for Subject
    RoleModel.objects.get_or_create(
        subject_club=math,
        name="Sir Isaac Newton",
        bio="Mathematician and physicist.",
        contribution="Universal gravitation and calculus."
    )

    # Practical for Subject
    PracticalApplication.objects.get_or_create(
        subject_club=math,
        title="Building a Calculator",
        description="Build a simple mechanical calculator using cardboard.",
        guide="1. Cut cardboard\n2. Label numbers\n3. Use rubber bands for gears"
    )

    # 3. Social Branch
    sports, _ = SocialGroup.objects.get_or_create(main_category=social_cat, name="Sports & Games", icon="⚽")
    
    football, _ = SocialClub.objects.get_or_create(
        group=sports,
        name="Football Club",
        description="Play and learn football tactics.",
        facilitator="Coach John",
        icon="⚽"
    )

    # Discussion for Social
    user, _ = User.objects.get_or_create(username="admin")
    ClubDiscussion.objects.get_or_create(
        social_club=football,
        user=user,
        content="When is the next match?"
    )

    # Role Model for Social
    RoleModel.objects.get_or_create(
        social_club=football,
        name="Lionel Messi",
        bio="Legendary footballer.",
        contribution="Won 8 Ballon d'Ors."
    )

    # 4. Teacher Branch
    admin_hubs, _ = TeacherCategory.objects.get_or_create(main_category=teacher_cat, name="Administrative Hubs")
    
    head_forum, _ = TeacherClub.objects.get_or_create(
        category=admin_hubs,
        name="Headteachers Forum",
        description="Leadership for school heads.",
        duration="12 months",
        icon="👨‍🏫"
    )

    # Topic for Teacher
    t2, _ = Topic.objects.get_or_create(teacher_club=head_forum, title="Resource Management", order=1)
    Lesson.objects.get_or_create(topic=t2, title="Budgeting 101", content_type="Workshop")

    print("Seeding Complete!")

if __name__ == "__main__":
    seed_educlubs()
