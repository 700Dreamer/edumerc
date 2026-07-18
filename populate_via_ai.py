#!/usr/bin/env python
import os
import sys
import json
import argparse
import requests
import django

# Set up Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from educlubs.models import Level, Subject, Topic, Subtopic, Lesson, Assessment, Question, Choice

OLLAMA_URL = "http://localhost:11434/api/generate"

def check_ollama(model_name):
    """Verify Ollama is running and the model is pulled."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("[ERROR] Ollama is not responding properly.")
            return False
        
        data = response.json()
        models = [m["name"] for m in data.get("models", [])]
        
        # Check matching model name (allowing tag differences like llama3 vs llama3:latest)
        pulled = False
        for m in models:
            if model_name in m or m in model_name:
                pulled = True
                break
                
        if not pulled:
            print(f"[WARNING] Model '{model_name}' not found in local Ollama instance.")
            print(f"Available models: {models}")
            print(f"Please run: 'ollama pull {model_name}' first if the script fails.")
        return True
    except Exception as e:
        print(f"[ERROR] Could not connect to Ollama on http://localhost:11434. Is it running? Error: {e}")
        return False

def generate_lesson_content(level, subject, topic, lesson_title, model_name):
    """Call Ollama to generate rich Markdown study notes."""
    prompt = f"""
You are an expert curriculum designer and educator in Uganda. Generate a comprehensive, high-quality, NCDC curriculum-aligned study note for a {level} student studying {subject}.

Topic: {topic}
Lesson Title: {lesson_title}

Requirements:
1. Write the content in clean Markdown format.
2. Start directly with '### 1. Introduction' or a relevant subheading. Do not write a title matching the lesson title (it is already displayed on the screen).
3. Include clear definitions, core concepts, bullet points, explanations, and worked examples where applicable.
4. Include at least one "Did You Know?" fun fact block using markdown blockquote syntax (e.g. `> Did You Know? [Fun fact details]`) to highlight interesting trivia.
5. Include at least one memorable quote, key highlight, or summary block in quotes using markdown blockquote syntax (e.g. `> "[Quote content]" - [Source/Explanation]`).
6. Keep the tone engaging and easy for a student of {level} level to understand.
7. Use LaTeX formatting for mathematical or scientific formulas (e.g., $x^2$ or $$E=mc^2$$) if applicable.
8. Do not include any conversational intro/outro remarks (e.g. "Sure! Here is the note:"). Output ONLY the markdown notes.
"""
    
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=data, timeout=180)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
    except Exception as e:
        print(f"  [ERROR] Ollama call failed for lesson '{lesson_title}': {e}")
    return None

def generate_lesson_questions(level, subject, topic, lesson_title, model_name):
    """Call Ollama to generate 2 multiple-choice questions in structured JSON format."""
    prompt = f"""
Generate exactly 2 multiple-choice questions to test a student's understanding of the lesson: '{lesson_title}' under the topic '{topic}' in {level} {subject}.

Output the questions in JSON format. The output MUST be a JSON object containing a single key "questions" which is a list of exactly 2 objects. Each question object must have:
- "text": The question text.
- "choices": An array of exactly 3 objects, each containing:
    - "text": The choice text.
    - "is_correct": Boolean (true/false) indicating if it is the correct answer. Exactly one choice in the array must be correct (is_correct=true).

Ensure the vocabulary and difficulty match a {level} student. Return ONLY the raw JSON object. Do not wrap in markdown codeblocks.
"""
    
    data = {
        "model": model_name,
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=data, timeout=180)
        if response.status_code == 200:
            result_str = response.json().get("response", "").strip()
            # Clean possible markdown JSON wrappers
            if result_str.startswith("```json"):
                result_str = result_str[7:]
            if result_str.endswith("```"):
                result_str = result_str[:-3]
            result_str = result_str.strip()
            return json.loads(result_str)
    except Exception as e:
        print(f"  [ERROR] Questions generation failed for lesson '{lesson_title}': {e}")
    return None

import django.db
from concurrent.futures import ThreadPoolExecutor

def process_single_lesson(lesson_id, model_name, index, total):
    """Worker function to process a single lesson in a separate thread."""
    from educlubs.models import Lesson, Assessment, Question, Choice
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
        subtopic = lesson.subtopic
        topic = subtopic.topic
        subject = topic.subject
        level = subject.level

        print(f"\n[{index}/{total}] Generating content for: {level.name} > {subject.name} > {topic.title} > {lesson.title}")

        # 1. Generate lesson notes
        notes = generate_lesson_content(level.name, subject.name, topic.title, lesson.title, model_name)
        if not notes:
            print(f"  [SKIP] Failed to generate lesson notes for: {lesson.title}")
            return
            
        # 2. Generate questions
        questions_data = generate_lesson_questions(level.name, subject.name, topic.title, lesson.title, model_name)
        
        # 3. Update lesson content
        lesson.content = notes
        lesson.save()
        print(f"  [SUCCESS] Updated lesson notes ({len(notes)} chars) for: {lesson.title}")

        # 4. Update questions
        questions_list = []
        if isinstance(questions_data, dict) and "questions" in questions_data:
            questions_list = questions_data["questions"]
        elif isinstance(questions_data, list):
            questions_list = questions_data
            
        if questions_list and isinstance(questions_list, list):
            assessment, _ = Assessment.objects.get_or_create(
                lesson=lesson,
                defaults={'title': f"Quiz on {lesson.title}", 'description': f"Evaluate learning for {lesson.title}."}
            )
            # Remove old placeholder questions
            assessment.questions.all().delete()
            
            q_created = 0
            for idx, q_item in enumerate(questions_list):
                if not isinstance(q_item, dict):
                    continue
                q_text = q_item.get("text")
                choices = q_item.get("choices", [])
                if not q_text or not choices:
                    continue
                    
                q_obj = Question.objects.create(
                    assessment=assessment,
                    text=q_text,
                    order=idx + 1
                )
                
                for c_item in choices:
                    Choice.objects.create(
                        question=q_obj,
                        text=c_item.get("text", ""),
                        is_correct=bool(c_item.get("is_correct", False))
                    )
                q_created += 1
            print(f"  [SUCCESS] Generated {q_created} quiz questions for: {lesson.title}")
        else:
            print(f"  [WARNING] Skipping question generation for {lesson.title} (invalid or empty JSON returned).")
    except Exception as e:
        print(f"  [ERROR] Failed to process lesson {lesson_id}: {e}")
    finally:
        # Close connection to release pool resource in thread
        django.db.connections.close_all()

def main():
    parser = argparse.ArgumentParser(description="Populate EduClubs curriculum using local Ollama model.")
    parser.add_argument("--model", type=str, default="llama3", help="Ollama model to use.")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of lessons to update (for testing).")
    parser.add_argument("--level", type=str, default=None, help="Filter by level (e.g. 'P.1', 'S.3').")
    parser.add_argument("--subject", type=str, default=None, help="Filter by subject name (e.g. 'Mathematics').")
    parser.add_argument("--force", action="store_true", help="Overwrite lessons even if they already have custom notes.")
    parser.add_argument("--workers", type=int, default=3, help="Number of concurrent threads to use.")
    args = parser.parse_args()

    if not check_ollama(args.model):
        sys.exit(1)

    # Fetch lessons that need population
    lessons = Lesson.objects.all()
    
    if args.level:
        lessons = lessons.filter(subtopic__topic__subject__level__name__iexact=args.level)
    if args.subject:
        lessons = lessons.filter(subtopic__topic__subject__name__icontains=args.subject)
        
    # Filter out S.2 (which is already detailed) unless forced
    if not args.force:
        lessons = lessons.exclude(subtopic__topic__subject__level__name='S.2')
        # Filter out lessons that already have long detailed content
        lessons = [l for l in lessons if len(l.content) < 500 or "Welcome to the module" in l.content or "Attempt past paper assessments" in l.content]
    
    lesson_ids = [l.id for l in lessons]
    if args.limit:
        lesson_ids = lesson_ids[:args.limit]
        
    total_lessons = len(lesson_ids)
    print(f"Found {total_lessons} lessons matching criteria that require AI-generated content.")
    
    if total_lessons == 0:
        print("No lessons need updating. Exiting.")
        return

    print(f"Starting concurrent generation using {args.workers} workers...")
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        for idx, lid in enumerate(lesson_ids):
            futures.append(executor.submit(process_single_lesson, lid, args.model, idx + 1, total_lessons))
            
        # Wait for all to complete
        for fut in futures:
            fut.result()

    print(f"\nAll done! Successfully updated {total_lessons} lessons.")

if __name__ == '__main__':
    main()
