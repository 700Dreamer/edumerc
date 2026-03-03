import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import Section, Level, Subject, Topic, Subtopic, Lesson, Assessment

def populate():
    print("Starting EduClubs population function...")

    # 1. Define Subjects
    primary_subjects = ["Mathematics", "English", "Science", "Social Studies"]
    secondary_subjects = ["Mathematics", "Biology", "Chemistry", "Physics", "History", "Geography", "ICT", "Literature"]

    print("Fetching sections...")
    sections = Section.objects.all()
    primary_section = sections.filter(name='Primary').first()
    secondary_section = sections.filter(name='Secondary').first()

    if not primary_section or not secondary_section:
        print("Required sections missing. Please run migrations first.")
        return

    print("Fetching levels...")
    levels = Level.objects.all()
    
    # 2. Populate Subjects for each Level
    print(f"Populating subjects for {levels.count()} levels...")
    for level in levels:
        subjects_to_add = primary_subjects if level.section == primary_section else secondary_subjects
        for i, sub_name in enumerate(subjects_to_add):
            subject, created = Subject.objects.get_or_create(
                name=sub_name,
                level=level,
                defaults={'order': i + 1, 'description': f"Standard {sub_name} for {level.name}"}
            )
            if created:
                print(f"  Created Subject: {subject}")

    # 3. Populate sample hierarchy for a few subjects (e.g. P.7 Science and S.4 Mathematics)
    # This avoids bloating the DB but demonstrates the full structure
    
    target_levels = Level.objects.filter(name__in=['P.7', 'S.4'])
    
    for level in target_levels:
        subjects = Subject.objects.filter(level=level)[:2] # Top 2 subjects
        for subject in subjects:
            print(f"Populating hierarchy for {subject}...")
            
            for t_idx in range(1, 4): # 3 Topics per subject
                topic, _ = Topic.objects.get_or_create(
                    title=f"{subject.name} Topic {t_idx}",
                    subject=subject,
                    defaults={
                        'description': f"Major unit covering key concepts in {subject.name}.",
                        'order': t_idx
                    }
                )
                
                for st_idx in range(1, 3): # 2 Subtopics per topic
                    subtopic, _ = Subtopic.objects.get_or_create(
                        title=f"Subtopic {t_idx}.{st_idx} of {topic.title}",
                        topic=topic,
                        defaults={
                            'description': f"Deep dive into specific area {st_idx}.",
                            'order': st_idx
                        }
                    )
                    
                    for l_idx in range(1, 3): # 2 Lessons per subtopic
                        lesson, _ = Lesson.objects.get_or_create(
                            title=f"Lesson {t_idx}.{st_idx}.{l_idx}: Mastery of {subtopic.title}",
                            subtopic=subtopic,
                            defaults={
                                'objectives': "- Understand core principles\n- Practice exercises\n- Final summary",
                                'content': f"Detailed instructional content for lesson {l_idx}. This includes theoretical explanations, diagrams, and examples.",
                                'video_url': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                                'duration_minutes': 45,
                                'order': l_idx,
                                'is_published': True
                            }
                        )
                        
                        # 1 Assessment per lesson
                        Assessment.objects.get_or_create(
                            title=f"Quiz: {lesson.title}",
                            lesson=lesson,
                            defaults={
                                'description': "A short multiple choice assessment to test understanding.",
                                'order': 1
                            }
                        )

    print("Population complete!")
    print(f"Subjects: {Subject.objects.count()}")
    print(f"Topics: {Topic.objects.count()}")
    print(f"Subtopics: {Subtopic.objects.count()}")
    print(f"Lessons: {Lesson.objects.count()}")
    print(f"Assessments: {Assessment.objects.count()}")

if __name__ == "__main__":
    populate()
