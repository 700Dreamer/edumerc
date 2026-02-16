import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIClient

def verify():
    client = APIClient()
    
    print("--- Main Categories ---")
    res = client.get('/api/v1/clubs/main-categories/')
    main_cats = res.data # It's a list since no pagination is forced
    print(json.dumps(main_cats, indent=2))
    
    # Get ID for 'Subject Clubs'
    subject_id = next(c['id'] for c in main_cats if 'Subject' in c['name'])
    
    print(f"\n--- Subcategories for Main Category {subject_id} (Subject) ---")
    res = client.get(f'/api/v1/clubs/sub-categories/?main_category={subject_id}')
    subs = res.data
    # Just print counts or a few
    print(f"Total subcategories found: {len(subs)}")
    p7_sub = next(s for s in subs if s['name'] == 'P7')
    print(f"P7 Subcategory ID: {p7_sub['id']}")
    
    print("--- 3. Get Real Clubs (Subject - P7) ---")
    res = client.get(f'/api/v1/clubs/clubs/?subcategory_id={p7_sub["id"]}&type=subject')
    clubs = res.data
    print(json.dumps(clubs, indent=2))

if __name__ == "__main__":
    verify()
