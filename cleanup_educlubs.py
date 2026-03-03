import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'educlubs_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    if not tables:
        print("No educlubs_ tables found.")
    else:
        print(f"Dropping {len(tables)} tables...")
        # Disable foreign key checks for the session if possible, or just drop in order/cascade
        # For PostgreSQL, we can use DROP TABLE ... CASCADE
        for table in tables:
            print(f"Dropping {table}...")
            cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
        
        # Also clean up migrations table for educlubs
        print("Cleaning up django_migrations...")
        cursor.execute("DELETE FROM django_migrations WHERE app = 'educlubs'")
        
        print("Cleanup complete.")
