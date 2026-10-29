"""
clean_database_notes.py
Ultra-fast bulk cleanup and normalization of study notes, lessons, and topics.
"""

import os
import sys
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.db import transaction
from educlubs.club_models import Note
from educlubs.models import Topic, Lesson

GARBAGE_HEADER_REGEX = re.compile(
    r'(^\d+\s+\d+.*Lcd)|'
    r'(^[A-Z0-9]{9,}:)|'
    r'(^A\s+B\s+C\s+A\s+B\s+C)|'
    r'(^E\s+O\s+E\b)|'
    r'(^127000025399K)|'
    r'(^\d+\s*:\s*(Core|Worked|Exam))',
    re.I
)

def clean_header_text(header):
    if not header:
        return header
    h = header.strip()
    h = re.sub(r'^(.*?)\s*-\s*\1\s*:\s*', r'\1: ', h, flags=re.I)
    h = re.sub(r'^(.*?)\s*-\s*\1$', r'\1', h, flags=re.I)
    h = re.sub(r'\bGodS\b', "God's", h)
    h = re.sub(r'\bTeacherS\b', "Teacher's", h)
    h = re.sub(r'\bLearnerS\b', "Learner's", h)
    h = re.sub(r'\bStudentS\b', "Student's", h)
    h = re.sub(r'\bNationS\b', "Nation's", h)
    h = re.sub(r'\bEarthS\b', "Earth's", h)
    h = re.sub(r'\s+', ' ', h).strip()
    return h

def clean_content_text(content):
    if not content:
        return content
    c = content
    c = re.sub(r'([A-Za-z]{2,})-\n\s*([a-z]{2,})', r'\1\2', c)
    c = re.sub(r'([A-Za-z]{3,})\n([a-z]{1,2})\b', r'\1\2', c)
    c = re.sub(r'[-=]{5,}', r'---', c)
    return c

def run_cleanup(dry_run=True):
    print("=" * 60)
    print(f"Running Fast Bulk Cleanup (dry_run={dry_run})")
    print("=" * 60)

    # 1. Notes
    notes = list(Note.objects.all())
    del_note_ids = []
    notes_to_update = []

    for n in notes:
        if GARBAGE_HEADER_REGEX.search(n.header):
            del_note_ids.append(n.id)
            continue
        new_h = clean_header_text(n.header)
        new_c = clean_content_text(n.content)
        if new_h != n.header or new_c != n.content:
            n.header = new_h
            n.content = new_c
            notes_to_update.append(n)

    print(f"Notes: {len(del_note_ids)} to delete, {len(notes_to_update)} to update.")

    # 2. Lessons
    lessons = list(Lesson.objects.all())
    del_lesson_ids = []
    lessons_to_update = []

    for l in lessons:
        if GARBAGE_HEADER_REGEX.search(l.title):
            del_lesson_ids.append(l.id)
            continue
        new_t = clean_header_text(l.title)
        new_c = clean_content_text(l.content)
        if new_t != l.title or new_c != l.content:
            l.title = new_t
            l.content = new_c
            lessons_to_update.append(l)

    print(f"Lessons: {len(del_lesson_ids)} to delete, {len(lessons_to_update)} to update.")

    # 3. Topics
    topics = list(Topic.objects.all())
    del_topic_ids = []
    topics_to_update = []

    for t in topics:
        if GARBAGE_HEADER_REGEX.search(t.title):
            del_topic_ids.append(t.id)
            continue
        new_t = clean_header_text(t.title)
        if new_t != t.title:
            t.title = new_t
            topics_to_update.append(t)

    print(f"Topics: {len(del_topic_ids)} to delete, {len(topics_to_update)} to update.")

    if not dry_run:
        with transaction.atomic():
            if del_note_ids:
                Note.objects.filter(id__in=del_note_ids).delete()
            if notes_to_update:
                Note.objects.bulk_update(notes_to_update, ['header', 'content'], batch_size=200)
            if del_lesson_ids:
                Lesson.objects.filter(id__in=del_lesson_ids).delete()
            if lessons_to_update:
                Lesson.objects.bulk_update(lessons_to_update, ['title', 'content'], batch_size=200)
            if del_topic_ids:
                Topic.objects.filter(id__in=del_topic_ids).delete()
            if topics_to_update:
                Topic.objects.bulk_update(topics_to_update, ['title'], batch_size=200)

        print("\n✓ Bulk cleanup successfully applied to the database!")
    else:
        print("\n[Dry run complete - no changes made]")

if __name__ == "__main__":
    is_live = "--live" in sys.argv
    run_cleanup(dry_run=not is_live)
