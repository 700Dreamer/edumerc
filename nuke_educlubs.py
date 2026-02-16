import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def nuke_educlubs():
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF")
        # List all possible educlubs tables
        tables = [
            'educlubs_maincategory', 
            'educlubs_subjectlevel', 
            'educlubs_subjectclub',
            'educlubs_topic',
            'educlubs_lesson',
            'educlubs_socialgroup',
            'educlubs_socialclub',
            'educlubs_clubdiscussion',
            'educlubs_teachercategory',
            'educlubs_teacherclub',
            'educlubs_rolemodel',
            'educlubs_practicalapplication',
            'educlubs_askaiquery',
            'educlubs_subcategory',
            'educlubs_club'
        ]
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"Dropped {table}")
            except Exception as e:
                print(f"Failed to drop {table}: {e}")
        
        cursor.execute("DELETE FROM django_migrations WHERE app='educlubs'")
        print("Cleared django_migrations for educlubs")

if __name__ == "__main__":
    nuke_educlubs()
