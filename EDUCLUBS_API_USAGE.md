# EduClubs API Usage Guide

The EduClubs API provides access to the structured academic hierarchy (Section → Level → Subject → Topic → Subtopic → Lesson → Assessment).

**Base URL:** `/api/v1/clubs/`

## 🏫 Sections
Represents the broad education categories (e.g., Primary, Secondary).

- **List Sections:** `GET /api/v1/clubs/sections/`
- **Detail:** `GET /api/v1/clubs/sections/{id}/`

---

## 🎓 Levels
Represents class levels within a section (e.g., P.1, S.4).

- **List Levels:** `GET /api/v1/clubs/levels/`
- **Filter by Section:** `GET /api/v1/clubs/levels/?section={section_id}`
- **Ordering:** `GET /api/v1/clubs/levels/?ordering=order`

---

## 📖 Subjects
Subjects belong to specific levels.

- **List Subjects:** `GET /api/v1/clubs/subjects/`
- **Filter by Level:** `GET /api/v1/clubs/subjects/?level={level_id}`
- **Detail (Includes Topics):** `GET /api/v1/clubs/subjects/{id}/`

---

## 🧩 Topics & Subtopics
Major syllabus units and their subdivisions.

- **List Topics:** `GET /api/v1/clubs/topics/?subject={subject_id}`
- **Topic Detail (Includes Subtopics):** `GET /api/v1/clubs/topics/{id}/`
- **List Subtopics:** `GET /api/v1/clubs/subtopics/?topic={topic_id}`
- **Subtopic Detail (Includes Lessons):** `GET /api/v1/clubs/subtopics/{id}/`

---

## 📝 Lessons & Assessments
The core instructional content.

- **List Lessons:** `GET /api/v1/clubs/lessons/?subtopic={subtopic_id}`
- **Lesson Detail (Includes Content & Assessments):** `GET /api/v1/clubs/lessons/{id}/`
- **Add Lesson:** `POST /api/v1/clubs/lessons/`

**Example Payload for Adding a Lesson:**
```json
{
    "title": "Introduction to Algebra",
    "subtopic": 5,
    "objectives": "- Understand variables\n- Solve simple equations",
    "content": "Full lesson text goes here...",
    "video_url": "https://example.com/video",
    "duration_minutes": 60,
    "order": 1,
    "is_published": true
}
```

- **List Assessments:** `GET /api/v1/clubs/assessments/?lesson={lesson_id}`

---

## 💡 Pro Tips
1. **Ordering**: Use `?ordering=order` on any list endpoint to get the items in their intended syllabus sequence.
2. **Details**: The `retrieve` (detail) endpoints for **Subject**, **Topic**, **Subtopic**, and **Lesson** are nested. For example, fetching a Subject detail will return the list of its Topics.
3. **Filtering**: All lists support filtering by their immediate parent ID.
