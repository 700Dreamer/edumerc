#!/usr/bin/env python
import os
import sys
import json
import argparse
import requests
import django
from concurrent.futures import ThreadPoolExecutor

# Set up Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import Club, RoleModel

OLLAMA_URL = "http://localhost:11434/api/generate"

def log_msg(msg):
    print(msg)
    sys.stdout.flush()

def get_role_models_for_club(club, model_name):
    subject = club.subject
    level = subject.level
    
    prompt = f'Generate exactly two inspiring role models for the school club: "{club.name}" at "{level.name}" level (Subject: {subject.name}). One role model must be of African/Ugandan descent and one must be a global figure. Write a detailed contribution (2-3 sentences) for each explaining who they are, what they achieved, and why they inspire students in this field. If you cannot find specific images, use working public domain/Wikipedia URLs or simple placeholder categories. Format your output as JSON matching this exact structure: {{"role_models": [{{"name": "Name 1", "contribution": "Contribution 1", "image_url": "https://..."}}, {{"name": "Name 2", "contribution": "Contribution 2", "image_url": "https://..."}}]}}'
    data = {
        "model": model_name,
        "prompt": prompt,
        "options": {
            "temperature": 0.1,
            "num_predict": 1024
        },
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=data, timeout=120)
        if response.status_code == 200:
            result_str = response.json().get("response", "").strip()
            # Extract JSON object from potential markdown / thoughts
            start_idx = result_str.find('{')
            end_idx = result_str.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = result_str[start_idx:end_idx+1]
                return json.loads(json_str)
            else:
                log_msg(f"  [ERROR] No JSON object found in Ollama response for club {club.name}. Raw: {result_str}")
    except Exception as e:
        log_msg(f"  [ERROR] Ollama call failed for club {club.name}: {e}")
    return None

import django.db

def process_single_club(club_id, model_name, index, total):
    try:
        club = Club.objects.get(pk=club_id)
        log_msg(f"[{index}/{total}] Fetching role models for club: {club.name} ({club.subject.level.name})")
        data = get_role_models_for_club(club, model_name)
        
        if not data or "role_models" not in data:
            log_msg(f"  [WARNING] Could not generate role models for: {club.name}")
            return
            
        role_models_list = data["role_models"]
        if not isinstance(role_models_list, list) or len(role_models_list) == 0:
            log_msg(f"  [WARNING] Invalid format or empty list for: {club.name}")
            return
            
        # Delete old role models for this club
        club.role_models.all().delete()
        
        created = 0
        for rm_item in role_models_list:
            name = rm_item.get("name")
            contribution = rm_item.get("contribution")
            img = rm_item.get("image_url")
            
            if not name or not contribution:
                continue
                
            RoleModel.objects.create(
                club=club,
                name=name,
                contribution=contribution,
                image=img
            )
            created += 1
            
        log_msg(f"  [SUCCESS] Created {created} unique role models for {club.name}.")
    except Exception as e:
        log_msg(f"  [ERROR] Failed to process club {club_id}: {e}")
    finally:
        django.db.connections.close_all()

def main():
    parser = argparse.ArgumentParser(description="Update role models for all clubs using Ollama.")
    parser.add_argument("--model", type=str, default="gemma4:12b", help="Ollama model to use.")
    parser.add_argument("--workers", type=int, default=2, help="Number of concurrent workers.")
    args = parser.parse_args()
    
    old_names = {'Albert Einstein', 'Marie Curie', 'Jane Goodall', 'Charles Darwin', 'Katherine Johnson', 'Isaac Newton', 'Chinua Achebe', 'William Shakespeare', 'Prof. Apolo Nsibambi', 'Wangari Maathai'}
    clubs = [c for c in Club.objects.all() if c.role_models.filter(name__in=old_names).exists() or c.role_models.count() < 2]
    club_ids = [c.id for c in clubs]
    total = len(club_ids)
    log_msg(f"Found {total} clubs that need role models updated.")
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        for idx, cid in enumerate(club_ids):
            futures.append(executor.submit(process_single_club, cid, args.model, idx + 1, total))
            
        for fut in futures:
            fut.result()
            
    log_msg("\nAll done! Successfully updated role models for all clubs.")

if __name__ == '__main__':
    main()
