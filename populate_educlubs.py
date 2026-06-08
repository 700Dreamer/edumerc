import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import (
    Section, Level, Subject, Topic, Subtopic, Lesson, Assessment,
    Club, Note, RoleModel, PracticalProject, DiscussionMessage,
    Question, Choice
)

def get_ugandan_curriculum(level_name, subject_name):
    is_primary = level_name.startswith('P.')
    is_olevel = level_name in ['S.1', 'S.2', 'S.3', 'S.4']
    is_alevel = level_name in ['S.5', 'S.6']
    
    try:
        level_num = int(level_name[2:])
    except:
        level_num = 1
        
    if is_primary:
        if "Mathematics" in subject_name:
            if level_num <= 3:
                return [
                    { "title": "Sorting and Matching", "lessons": [("Sorting Objects", "Practice", 20)] },
                    { "title": "Counting 1-100", "lessons": [("Number Sequences", "Video Lesson", 15)] },
                    { "title": "Simple Addition & Subtraction", "lessons": [("Adding Objects", "Interactive Quiz", 20)] }
                ]
            elif level_num <= 5:
                return [
                    { "title": "Sets", "lessons": [("Forming Sets", "Video Lesson", 20)] },
                    { "title": "Whole Numbers", "lessons": [("Place Values", "Practice", 25), ("Multiplication Tables", "Interactive Quiz", 20)] },
                    { "title": "Fractions", "lessons": [("Proper Fractions", "Video Lesson", 20)] },
                    { "title": "Geometry", "lessons": [("Shapes and Angles", "Practice", 15)] }
                ]
            else:
                return [
                    { "title": "Sets and Venn Diagrams", "lessons": [("Intersection and Union", "Video Lesson", 25)] },
                    { "title": "Operations on Whole Numbers", "lessons": [("BODMAS", "Practice", 30)] },
                    { "title": "Decimals and Percentages", "lessons": [("Conversions", "Interactive Quiz", 20)] },
                    { "title": "Integers", "lessons": [("Number Lines", "Video Lesson", 20)] },
                    { "title": "Geometry", "lessons": [("Properties of Polygons", "Practice", 25)] }
                ]
        elif "English" in subject_name:
            if level_num <= 3:
                return [
                    { "title": "Phonics", "lessons": [("Letter Sounds", "Video Lesson", 15)] },
                    { "title": "Vocabulary", "lessons": [("Things in the Classroom", "Interactive Quiz", 20)] },
                    { "title": "Handwriting", "lessons": [("Forming Letters", "Practice", 15)] }
                ]
            else:
                return [
                    { "title": "Grammar", "lessons": [("Tenses", "Video Lesson", 20), ("Parts of Speech", "Practice", 25)] },
                    { "title": "Comprehension", "lessons": [("Reading Passages", "Reading Material", 30)] },
                    { "title": "Composition", "lessons": [("Writing Letters", "Practice", 35)] }
                ]
        elif "Science" in subject_name:
            if level_num <= 3:
                return [
                    { "title": "Personal Hygiene", "lessons": [("Cleaning the Body", "Video Lesson", 15)] },
                    { "title": "Our Environment", "lessons": [("Things Around Us", "Interactive Quiz", 20)] },
                    { "title": "Plants and Animals", "lessons": [("Domestic Animals", "Video Lesson", 20)] }
                ]
            else:
                return [
                    { "title": "Human Body Systems", "lessons": [("The Digestive System", "Video Lesson", 25), ("The Respiratory System", "Reading Material", 20)] },
                    { "title": "Matter and Energy", "lessons": [("States of Matter", "Simulation", 20)] },
                    { "title": "Sanitation", "lessons": [("Keeping the Community Clean", "Practice", 15)] },
                    { "title": "Immunization", "lessons": [("Childhood Diseases", "Reading Material", 20)] }
                ]
        elif "Studies" in subject_name or "SST" in subject_name:
            if level_num <= 3:
                return [
                    { "title": "Our School", "lessons": [("People in our School", "Video Lesson", 15)] },
                    { "title": "Our Home", "lessons": [("Roles of Family Members", "Interactive Quiz", 15)] },
                    { "title": "Our Neighborhood", "lessons": [("Important Places", "Practice", 20)] }
                ]
            elif level_num == 4:
                return [
                    { "title": "Location of our District", "lessons": [("Using a Map", "Practice", 25)] },
                    { "title": "Leaders in our District", "lessons": [("Local Councils", "Reading Material", 20)] }
                ]
            elif level_num == 5:
                return [
                    { "title": "Physical Features of Uganda", "lessons": [("Mountains and Lakes", "Video Lesson", 30)] },
                    { "title": "History of Uganda", "lessons": [("Pre-colonial Societies", "Reading Material", 25)] }
                ]
            else:
                return [
                    { "title": "Physical Features of East Africa", "lessons": [("The Rift Valley", "Video Lesson", 25)] },
                    { "title": "The People of East Africa", "lessons": [("Ethnic Groups", "Reading Material", 20)] },
                    { "title": "Independence Movements", "lessons": [("Struggle for Freedom", "Video Lesson", 30)] }
                ]
        elif "Religious" in subject_name:
            return [
                { "title": "God's Creation", "lessons": [("The Story of Creation", "Reading Material", 20)] },
                { "title": "Living in Peace", "lessons": [("Forgiveness", "Story", 15)] }
            ]

    elif is_olevel:
        if "Mathematics" in subject_name:
            if level_num == 1:
                return [
                    { "title": "Natural Numbers", "lessons": [("Factors and Multiples", "Practice", 30)] },
                    { "title": "Fractions & Decimals", "lessons": [("Operations on Fractions", "Video Lesson", 25)] },
                    { "title": "Algebraic Expressions", "lessons": [("Simplifying Expressions", "Interactive Quiz", 20)] }
                ]
            elif level_num == 4:
                return [
                    { "title": "Matrices", "lessons": [("Matrix Multiplication", "Practice", 35)] },
                    { "title": "Trigonometry", "lessons": [("Sine & Cosine Rules", "Video Lesson", 30)] },
                    { "title": "Vectors", "lessons": [("Addition of Vectors", "Interactive Quiz", 25)] },
                    { "title": "Statistics", "lessons": [("Histograms and Ogives", "Simulation", 40)] }
                ]
            else:
                return [
                    { "title": "Sets", "lessons": [("Venn Diagrams", "Video Lesson", 30)] },
                    { "title": "Simultaneous Equations", "lessons": [("Substitution and Elimination", "Practice", 40)] },
                    { "title": "Geometry", "lessons": [("Circle Properties", "Interactive Quiz", 25)] }
                ]
        elif "English" in subject_name:
            return [
                { "title": "Summary Writing", "lessons": [("Identifying Main Points", "Practice", 25)] },
                { "title": "Letter Writing", "lessons": [("Formal Letters", "Practice", 30)] },
                { "title": "Comprehension", "lessons": [("Analyzing Texts", "Video Lesson", 25)] },
                { "title": "Essay Writing", "lessons": [("Descriptive Essays", "Practice", 35)] }
            ]
        elif "Physics" in subject_name:
            if level_num == 1:
                return [
                    { "title": "Measurements", "lessons": [("SI Units", "Reading Material", 20), ("Measuring Instruments", "Simulation", 25)] },
                    { "title": "Matter", "lessons": [("States of Matter", "Video Lesson", 20)] }
                ]
            elif level_num == 4:
                return [
                    { "title": "Electricity", "lessons": [("Ohm's Law", "Simulation", 30)] },
                    { "title": "Magnetism", "lessons": [("Electromagnetic Induction", "Video Lesson", 35)] },
                    { "title": "Modern Physics", "lessons": [("Cathode Rays", "Reading Material", 20)] }
                ]
            else:
                return [
                    { "title": "Mechanics", "lessons": [("Newton's Laws", "Video Lesson", 30)] },
                    { "title": "Heat", "lessons": [("Specific Heat Capacity", "Practice", 25)] },
                    { "title": "Optics", "lessons": [("Lenses", "Simulation", 30)] }
                ]
        elif "Chemistry" in subject_name:
            if level_num == 1:
                return [
                    { "title": "Introduction to Chemistry", "lessons": [("Laboratory Apparatus", "Simulation", 20)] },
                    { "title": "Mixtures", "lessons": [("Separation Techniques", "Video Lesson", 25)] }
                ]
            else:
                return [
                    { "title": "Atomic Structure", "lessons": [("Isotopes", "Reading Material", 20)] },
                    { "title": "Acids and Bases", "lessons": [("Titration", "Simulation", 30)] },
                    { "title": "Carbon Chemistry", "lessons": [("Hydrocarbons", "Video Lesson", 25)] }
                ]
        elif "Biology" in subject_name:
            return [
                { "title": "Cell Biology", "lessons": [("Plant and Animal Cells", "Video Lesson", 20)] },
                { "title": "Nutrition", "lessons": [("Photosynthesis", "Simulation", 25), ("Human Digestive System", "Interactive Quiz", 20)] },
                { "title": "Ecology", "lessons": [("Food Chains", "Reading Material", 15)] }
            ]
        elif "Geography" in subject_name:
            return [
                { "title": "Map Reading", "lessons": [("Grid References", "Practice", 30)] },
                { "title": "Physical Geography", "lessons": [("Internal Land-forming Processes", "Video Lesson", 35)] }
            ]
        elif "History" in subject_name:
            return [
                { "title": "Pre-colonial Era", "lessons": [("Migration of the Bantu", "Video Lesson", 30)] },
                { "title": "Colonial Rule", "lessons": [("Indirect Rule", "Reading Material", 25)] }
            ]
        elif "Technology" in subject_name or "ICT" in subject_name:
            return [
                { "title": "Word Processing", "lessons": [("Formatting", "Practice", 30)] },
                { "title": "Spreadsheets", "lessons": [("Formulas", "Video Lesson", 30)] }
            ]
        elif "Entrepreneurship" in subject_name:
            return [
                { "title": "Business Planning", "lessons": [("Writing a Plan", "Practice", 35)] },
                { "title": "Accounting", "lessons": [("Cash Books", "Practice", 40)] }
            ]

    elif is_alevel:
        if "Mathematics" in subject_name:
            return [
                { "title": "Pure Math: Calculus", "lessons": [("Integration", "Video Lesson", 45)] },
                { "title": "Mechanics", "lessons": [("Projectiles", "Video Lesson", 40)] }
            ]
        elif "Physics" in subject_name:
            return [
                { "title": "Advanced Mechanics", "lessons": [("Rotational Dynamics", "Video Lesson", 40)] },
                { "title": "Quantum Physics", "lessons": [("Photoelectric Effect", "Interactive Quiz", 30)] }
            ]
        elif "Chemistry" in subject_name:
            return [
                { "title": "Physical Chemistry", "lessons": [("Rate Laws", "Video Lesson", 35)] },
                { "title": "Organic Chemistry", "lessons": [("Alkanes", "Practice", 30)] }
            ]
        elif "Biology" in subject_name:
            return [
                { "title": "Genetics", "lessons": [("DNA Replication", "Simulation", 35)] },
                { "title": "Physiology", "lessons": [("Nervous System", "Video Lesson", 40)] }
            ]
        elif "Economics" in subject_name:
            return [
                { "title": "Microeconomics", "lessons": [("Demand and Supply", "Video Lesson", 35)] },
                { "title": "Macroeconomics", "lessons": [("National Income", "Practice", 40)] }
            ]
        elif "Literature" in subject_name:
            return [
                { "title": "Poetry Analysis", "lessons": [("Poetic Devices", "Video Lesson", 30)] },
                { "title": "Plays", "lessons": [("Shakespearean Tragedy", "Practice", 40)] }
            ]
        elif "Paper" in subject_name:
            return [
                { "title": "Critical Thinking", "lessons": [("Constructing Arguments", "Practice", 30)] },
                { "title": "Essay Writing", "lessons": [("Structuring an Essay", "Video Lesson", 40)] }
            ]

    return [
        { "title": f"General Introduction to {subject_name}", "lessons": [("Overview Lecture", "Video Lesson", 30)] },
        { "title": "Review of Core Principles", "lessons": [("Preparation Quiz", "Interactive Quiz", 15)] }
    ]

def populate():
    print("Starting EduClubs database seeding...")

    # 1. Fetch/Create Sections
    print("Checking Sections...")
    primary_section, _ = Section.objects.get_or_create(
        name='Primary',
        defaults={'description': 'Primary Education Section'}
    )
    secondary_section, _ = Section.objects.get_or_create(
        name='Secondary',
        defaults={'description': 'Secondary Education Section'}
    )

    # 2. Seed/Verify Levels (P.1 - P.7, S.1 - S.6)
    print("Checking Levels...")
    for i in range(1, 8):
        Level.objects.get_or_create(
            name=f'P.{i}',
            section=primary_section,
            defaults={'order': i}
        )
    for i in range(1, 5):
        Level.objects.get_or_create(
            name=f'S.{i}',
            section=secondary_section,
            defaults={'order': i + 10}
        )
    for i in range(5, 7):
        Level.objects.get_or_create(
            name=f'S.{i}',
            section=secondary_section,
            defaults={'order': i + 10}
        )

    levels = Level.objects.all().order_by('order')
    print(f"Levels in system: {[(l.id, l.name) for l in levels]}")

    # 3. Fetch/Create default user for discussion messages
    from django.contrib.auth import get_user_model
    User = get_user_model()
    default_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    if not default_user:
        default_user = User.objects.create_user(
            username="edu_explorer",
            email="explorer@edumerc.com",
            password="password123",
            first_name="Luke",
            last_name="Nyanja",
            role="STUDENT"
        )

    primary_subjects = [
        ("Mathematics", "Calculator"),
        ("English Language", "Book"),
        ("Integrated Science", "FlaskConical"),
        ("Social Studies (SST)", "Globe"),
        ("Religious Education", "BookOpen")
    ]
    olevel_subjects = [
        ("Mathematics", "Calculator"),
        ("English Language", "PenTool"),
        ("Physics", "Zap"),
        ("Chemistry", "TestTube"),
        ("Biology", "Microscope"),
        ("Geography", "Map"),
        ("History", "ScrollText"),
        ("Information and Communications Technology (ICT)", "Monitor"),
        ("Entrepreneurship Education", "Briefcase")
    ]
    alevel_subjects = [
        ("Mathematics", "Calculator"),
        ("Physics", "Zap"),
        ("Chemistry", "TestTube"),
        ("Biology", "Microscope"),
        ("Economics", "TrendingUp"),
        ("Literature in English", "BookOpen"),
        ("General Paper", "Newspaper")
    ]

    # 4. Populate Subjects, Curriculum, and Clubs
    print("Populating subjects, curriculum, and clubs...")
    for level in levels:
        if level.section == primary_section:
            subjects_to_add = primary_subjects
        elif level.name in ['S.1', 'S.2', 'S.3', 'S.4']:
            subjects_to_add = olevel_subjects
        else:
            subjects_to_add = alevel_subjects

        for idx, (sub_name, icon_name) in enumerate(subjects_to_add):
            subject, _ = Subject.objects.get_or_create(
                name=sub_name,
                level=level,
                defaults={'order': idx + 1, 'description': f"Standard {sub_name} for {level.name}"}
            )

            # Clean existing curriculum topics to prevent duplicates
            Topic.objects.filter(subject=subject).delete()

            # Create dynamic Ugandan curriculum topics and lessons
            topics_data = get_ugandan_curriculum(level.name, sub_name)
            for t_idx, topic_info in enumerate(topics_data):
                topic = Topic.objects.create(
                    title=topic_info["title"],
                    subject=subject,
                    description=f"Standard unit covering {topic_info['title']} in {sub_name}.",
                    order=t_idx + 1
                )
                subtopic = Subtopic.objects.create(
                    title=f"Core Concepts: {topic.title}",
                    topic=topic,
                    description=f"Detailed study elements of {topic.title}.",
                    order=1
                )
                for l_idx, (l_title, l_type, l_duration) in enumerate(topic_info["lessons"]):
                    lesson_content = (
                        f"### {l_title} Study Note\n\n"
                        f"Welcome to the module on **{l_title}**. Here, we discuss the core fundamentals of "
                        f"**{topic.title}** according to the Ugandan National Curriculum (NCDC) guidelines.\n\n"
                        f"#### Detailed Explanation\n"
                        f"1. Review the primary definitions and equations.\n"
                        f"2. Note standard formulas and complete practical experiments.\n"
                        f"3. Attempt past paper assessments and consult tutor guidelines.\n\n"
                        f"#### Revision Checklist\n"
                        f"- [ ] Active recall of definitions.\n"
                        f"- [ ] Form study groups to discuss key exercises.\n"
                        f"- [ ] Request feedback from your verified Coach."
                    )
                    lesson = Lesson.objects.create(
                        title=l_title,
                        subtopic=subtopic,
                        objectives=f"- Gain expertise in {l_title}.\n- Understand application principles.",
                        content=lesson_content,
                        duration_minutes=l_duration,
                        order=l_idx + 1,
                        is_published=True
                    )
                    assessment = Assessment.objects.create(
                        title=f"Quiz on {lesson.title}",
                        lesson=lesson,
                        description=f"Standard multiple-choice assessment to evaluate learning outcomes for {lesson.title}.",
                        order=1
                    )
                    
                    # Seed multiple-choice questions & options
                    q1 = Question.objects.create(
                        assessment=assessment,
                        text=f"What is the primary concept covered in the lesson: '{lesson.title}'?",
                        order=1
                    )
                    Choice.objects.create(question=q1, text="The correct core definition of this topic.", is_correct=True)
                    Choice.objects.create(question=q1, text="An unrelated concept.", is_correct=False)
                    Choice.objects.create(question=q1, text="A completely wrong alternative.", is_correct=False)
                    
                    q2 = Question.objects.create(
                        assessment=assessment,
                        text=f"Which of the following is true regarding '{lesson.title}'?",
                        order=2
                    )
                    Choice.objects.create(question=q2, text="True statement matching syllabus guidelines.", is_correct=True)
                    Choice.objects.create(question=q2, text="False statement.", is_correct=False)

            # Create Club with deterministic ID and direct Subject ForeignKey link
            club_id = level.id * 100 + (idx + 1)
            description = f"Connect with other students interested in {sub_name}. Improve your performance in {level.name} examinations."
            
            club, created = Club.objects.get_or_create(
                id=club_id,
                defaults={
                    'name': sub_name,
                    'icon': icon_name,
                    'description': description,
                    'level': level,
                    'type': 'subject',
                    'popular': (idx == 0 or idx == 2)
                }
            )
            club.subject = subject
            club.save()
            
            if created:
                print(f"  Created Club: {club.name} (ID: {club.id}) for Level: {level.name}")
                
                # Seed Club Notes
                Note.objects.create(
                    club=club,
                    header=f"Core Concepts of {sub_name}",
                    content=f"### Study Guide for {sub_name}\n\nWelcome to the {sub_name} club notes. In this module, we focus on the essential topics required for {level.name} assessments.\n\n#### Key Objectives\n1. Master the standard formulas and theories.\n2. Apply concepts to NCDC mock paper queries.\n3. Collaborate with study groups to review past questions."
                )
                Note.objects.create(
                    club=club,
                    header=f"{sub_name} Revision Notes",
                    content=f"### Revision Strategy\n\nEnsure you active-recall these sections:\n- Use flashcards for core terms.\n- Attempt the practice quizzes at the end of each lesson.\n- Reach out to our verified coaches for prompt support."
                )

                # Seed Role Models
                if "Math" in sub_name:
                    role_models = [
                        ("Katherine Johnson", "NASA Mathematician whose orbital calculations were critical to US spaceflights.", "https://upload.wikimedia.org/wikipedia/commons/6/6d/Katherine_Johnson_1983.jpg"),
                        ("Isaac Newton", "Physicist who developed calculus and classical mechanics.", "https://upload.wikimedia.org/wikipedia/commons/3/39/GodfreyKneller-IsaacNewton-1689.jpg")
                    ]
                elif "English" in sub_name or "Literature" in sub_name:
                    role_models = [
                        ("Chinua Achebe", "Renowned Nigerian novelist who wrote 'Things Fall Apart'.", "https://upload.wikimedia.org/wikipedia/commons/1/10/Chinua_Achebe_-_Buffalo_2008_1.jpg"),
                        ("William Shakespeare", "Classic English playwright and poet.", "https://upload.wikimedia.org/wikipedia/commons/a/a2/Shakespeare.jpg")
                    ]
                elif "Science" in sub_name or "Physics" in sub_name or "Chemistry" in sub_name:
                    role_models = [
                        ("Albert Einstein", "Theoretical physicist who formulated the theory of relativity.", "https://upload.wikimedia.org/wikipedia/commons/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg"),
                        ("Marie Curie", "Pioneered radioactivity research and won two Nobel Prizes.", "https://upload.wikimedia.org/wikipedia/commons/c/c8/Marie_Curie_c._1920s.jpg")
                    ]
                elif "Biology" in sub_name:
                    role_models = [
                        ("Dr. Jane Goodall", "World-renowned primatologist and environmental activist.", "https://upload.wikimedia.org/wikipedia/commons/8/87/Jane_Goodall_2015.jpg"),
                        ("Charles Darwin", "Famous naturalist who proposed the theory of evolution.", "https://upload.wikimedia.org/wikipedia/commons/2/2e/Charles_Darwin_seated_crop.jpg")
                    ]
                else:
                    role_models = [
                        ("Prof. Apolo Nsibambi", "Eminent Ugandan scholar and statesman.", "https://images.unsplash.com/photo-1537511446984-935f663eb1f4?auto=format&fit=crop&q=80&w=200"),
                        ("Wangari Maathai", "Nobel laureate and founder of Green Belt Movement.", "https://upload.wikimedia.org/wikipedia/commons/6/64/Wangari_Maathai_2001_1.jpg")
                    ]

                for name, contribution, img in role_models:
                    RoleModel.objects.create(
                        club=club,
                        name=name,
                        contribution=contribution,
                        image=img
                    )

                # Seed Practical Project with download guide URL
                PracticalProject.objects.update_or_create(
                    club=club,
                    defaults={
                        'title': f"Hands-on {sub_name} Project",
                        'description': f"Conduct a self-guided practical project to explore {sub_name} in action.",
                        'steps': [
                            "Review current class notes and guidelines.",
                            "Gather simple household materials.",
                            "Perform the experiment / write the summary.",
                            "Share your findings in the Discussion forum for coach review."
                        ],
                        'guide_url': "https://edumerc.up.railway.app/media/guides/sample_guide.pdf"
                    }
                )

                # Seed Discussion Comments with user ForeignKeys
                DiscussionMessage.objects.create(
                    club=club,
                    user=default_user,
                    comment=f"Hello! When are we starting the revision topic for {sub_name}?",
                    time=timezone.now() - timedelta(hours=2)
                )
                DiscussionMessage.objects.create(
                    club=club,
                    user=default_user,
                    comment=f"We will begin Term 1 reviews next Monday. Check study resources in the sidebar!",
                    time=timezone.now() - timedelta(hours=1)
                )

    print("EduClubs database seeding completed successfully!")

if __name__ == "__main__":
    populate()
