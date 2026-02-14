import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import Club, Topic, Lesson, RoleModel, PracticalApplication, ClubDiscussion

def populate_clubs():
    # 1. Science Club (Subject, P5)
    science_club, created = Club.objects.get_or_create(
        name="Junior Science Club",
        defaults={
            'category': 'Subject',
            'level': 'P5',
            'description': 'Exploring the wonders of science for Primary 5 students.'
        }
    )
    print(f"Club: {science_club.name}")

    # Role Model
    RoleModel.objects.get_or_create(
        club=science_club,
        name="Isaac Newton",
        defaults={
            'bio': 'English mathematician, physicist, astronomer, theologian, and author.',
            'contribution': 'Formulated the laws of motion and universal gravitation.'
        }
    )

    # Topics & Lessons
    topic1, _ = Topic.objects.get_or_create(club=science_club, title="Photosynthesis", order=1)
    Lesson.objects.get_or_create(
        topic=topic1,
        title="What is Photosynthesis?",
        defaults={'content_type': 'Text', 'text_content': 'Photosynthesis is the process used by plants...', 'order': 1}
    )
    
    topic2, _ = Topic.objects.get_or_create(club=science_club, title="The Solar System", order=2)
    Lesson.objects.get_or_create(
        topic=topic2,
        title="Planet Earth",
        defaults={'content_type': 'Text', 'text_content': 'Earth is the third planet from the Sun...', 'order': 1}
    )

    # Practical App
    PracticalApplication.objects.get_or_create(
        club=science_club,
        title="Grow a Bean Plant",
        defaults={
            'description': 'Observe the growth of a bean plant over 2 weeks.',
            'guide': '1. Get a bean. 2. Plant it in soil. 3. Water it daily.'
        }
    )

    # 2. Debate Club (Social, General)
    debate_club, created = Club.objects.get_or_create(
        name="High School Debate Club",
        defaults={
            'category': 'Social',
            'level': 'S3', # Could be general but let's make it S3 for variety
            'description': 'Sharpen your argumentation and public speaking skills.'
        }
    )
    print(f"Club: {debate_club.name}")

    Topic.objects.get_or_create(club=debate_club, title="Public Speaking Basics", order=1)

    # 3. Mathematics Club (Subject, S4)
    math_club, created = Club.objects.get_or_create(
        name="O-Level Math Whizzes",
        defaults={
            'category': 'Subject',
            'level': 'S4',
            'description': 'Advanced mathematics for O-Level candidates.'
        }
    )
    print(f"Club: {math_club.name}")

    Topic.objects.get_or_create(club=math_club, title="Quadratic Equations", order=1)
    Topic.objects.get_or_create(club=math_club, title="Vectors and Matrices", order=2)

    # 4. Teachers Forum (Teacher, General)
    teacher_club, created = Club.objects.get_or_create(
        name="Science Teachers Network",
        defaults={
            'category': 'Teacher',
            'level': 'General',
            'description': 'A community for science teachers to share resources.'
        }
    )
    print(f"Club: {teacher_club.name}")

if __name__ == '__main__':
    print("Populating Educlubs data...")
    populate_clubs()
    print("Done!")
