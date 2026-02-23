import os
import sys
import django

# Setup path and environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def run_script(module_name, func_name=None):
    print(f"\n--- Running {module_name} ---")
    try:
        module = __import__(module_name)
        if func_name:
            getattr(module, func_name)()
        else:
            # If no function specified, assume it runs on import if protected by __main__
            # or try a default 'populate' or 'seed' function
            for candidate in ['populate', 'seed', 'populate_schools', 'seed_educlubs', 'populate_clubs']:
                if hasattr(module, candidate):
                    getattr(module, candidate)()
                    return
            print(f"  Warning: No recognizable entry function found in {module_name}")
    except Exception as e:
        print(f"  Error running {module_name}: {e}")

if __name__ == "__main__":
    print("Starting master population process...")
    
    # 1. Edupedia (Schools)
    run_script('populate_schools', 'populate_schools')
    
    # 2. EduShop (Products)
    # populate_products doesn't have a function, it runs on import if path is set
    # but we are already in the same process, so we can just run its code or wrap it
    run_script('populate_products')
    
    # 3. EduClubs (Clubs)
    run_script('seed_educlubs', 'seed_educlubs')
    
    # 4. EduCoach (Coaches, Sessions)
    run_script('populate_educoach', 'populate')
    
    # 5. Remaining (Funds, Quests)
    run_script('populate_remaining', 'populate_remaining')
    
    print("\nMaster population complete!")
