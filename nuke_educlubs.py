import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def nuke_educlubs():
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF")
        # Tables to drop
        tables = [
            'educlubs_maincategory', 
            'educlubs_subcategory', 
            'educlubs_club',
            'educlubs_socialcategory',
            'educlubs_teacherhubcategory',
            'educlubs_subjectcategory',
            'educlubs_clubcategory',
            'educlubs_topic',
            'educlubs_lesson',
            'educlubs_rolemodel',
            'educlubs_practicalapplication',
            'educlubs_clubdiscussion',
            'educlubs_askaiquery'
        ]
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE {table}")
                print(f"Dropped {table}")
            except Exception as e:
                print(f"Failed to drop {table}: {e}")
        
        # Clear migration history for educlubs
        cursor.execute("DELETE FROM django_migrations WHERE app='educlubs'")
        print("Cleared django_migrations for educlubs")

if __name__ == "__main__":
    nuke_educlubs()
