## Student & Course Management CLI System

A Python-based command-line interface (CLI) application for managing student records, course information, and student-course enrollments. Built using SQLAlchemy ORM for persistent SQLite storage and Rich for formatted terminal output.

## Features

Student Management: Create, list, update, and delete student records (ID, Name, Academic Level, Department).

Course Management: Add, list, update, and delete available courses and assigned instructors.

Enrollment System: Link students to courses with automated enrollment date tracking (datetime.date.today()) and duplicate protection via unique database constraints.

Input Validation: Custom CLI validators enforcing minimum character lengths, numeric constraints (academic level 1–5), character restrictions, and confirmation prompts before deletions.

Terminal UI: Clear table structures and styled notifications using the rich library.

Data Integrity: Cascade deletion support via SQLAlchemy relationships (all, delete-orphan) and relational models using standard SQLite constraints.

## Database Architecture

```
The application uses an SQLite database (StudentCourse.db) managed through SQLAlchemy ORM models:

+-------------------+       +--------------------+       +------------------+
|      Student      |       |     Enrollment     |       |      Course      |
+-------------------+       +--------------------+       +------------------+
| PK  stuID         |<----->| PK, FK  stuID      |       | PK  courseID     |
|     name          |       | PK, FK  courseID   |<----->|     course_name  |
|     level         |       |         date_enrolled      |     instructor   |
|     dept          |       +--------------------+       +------------------+
+-------------------+

```
---
## Tech Stack

Language: Python 3.x

ORM: SQLAlchemy

Database: SQLite

Terminal UI: Rich


---

## CLI Menu Options

--------------------------- Student Course System ---------------------------
1. Add Student         5. Add Course          9. Enroll Student
2. List Students        6. List Courses        10. List Enrollments
3. Update Student      7. Update Course       11. Delete Enrollment
4. Delete Student      8. Delete Course       12. Exit

---

### Author:
Hagar Mahmoud (AI & ML student)