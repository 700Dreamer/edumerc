import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("Django setup successful")
from educlubs.models import Section
print(f"Section count: {Section.objects.count()}")
