import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'educlubs_%'")
    tables = cursor.fetchall()
    print("Found tables:")
    for table in tables:
        print(f"- {table[0]}")
