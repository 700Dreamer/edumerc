import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import json
from rest_framework.test import APIClient

def verify():
    client = APIClient()
    print("\n--- 1. Main Categories ---")
    res = client.get('/api/v1/clubs/main-categories/')
    print(json.dumps(res.data, indent=2))

    if not res.data:
        print("No main categories found. Seeding might have failed.")
        return

    subject_cat = res.data[0]
    print(f"\n--- 2. Subcategories for Main Category {subject_cat['id']} (Subject) ---")
    res = client.get(f'/api/v1/clubs/sub-categories/?main_category={subject_cat["id"]}')
    print(f"Total subcategories found: {len(res.data)}")
    
    p7_sub = next((s for s in res.data if s['name'] == 'P7'), None)
    if p7_sub:
        print(f"P7 Subcategory ID: {p7_sub['id']}")
        
        print(f"\n--- 3. List Clubs (Subject - P7) ---")
        res = client.get(f'/api/v1/clubs/clubs/?subcategory_id={p7_sub["id"]}&type=subject')
        print(json.dumps(res.data, indent=2))
        
        if res.data:
            math_club_id = res.data[0]['id']
            print(f"\n--- 4. GET Single Club Detail (Math Club - Subject) ---")
            res = client.get(f'/api/v1/clubs/clubs/{math_club_id}/?type=subject')
            print(json.dumps(res.data, indent=2))
            
            # Check for contract keys
            keys = res.data.keys()
            expected = ['curriculum', 'roleModels', 'discussion', 'practical']
            for k in expected:
                if k in keys:
                    print(f"✅ Found contract key: {k}")
                else:
                    print(f"❌ Missing contract key: {k}")

    print(f"\n--- 5. GET Single Club Detail (Social - Football) ---")
    # We'll just try id 1 for social since we seeded it
    res = client.get(f'/api/v1/clubs/clubs/1/?type=social')
    if res.status_code == 200:
        print(json.dumps(res.data, indent=2))
    else:
        print(f"Social Club Detail failed with status {res.status_code}")

if __name__ == "__main__":
    verify()
