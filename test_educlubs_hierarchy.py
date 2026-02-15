import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import SocialCategory, TeacherHubCategory, SubjectCategory
from educlubs.serializers import SocialCategoryHierarchySerializer, TeacherHubCategoryHierarchySerializer, SubjectCategoryHierarchySerializer

def test_hierarchy():
    social = SocialCategory.objects.prefetch_related('clubs').all()
    teachers = TeacherHubCategory.objects.prefetch_related('clubs').all()
    subjects = SubjectCategory.objects.prefetch_related('clubs').all()
    
    data = {
        "Social Clubs": SocialCategoryHierarchySerializer(social, many=True).data,
        "Teacher Hubs": TeacherHubCategoryHierarchySerializer(teachers, many=True).data,
        "Subject Clubs": SubjectCategoryHierarchySerializer(subjects, many=True).data
    }
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    test_hierarchy()
