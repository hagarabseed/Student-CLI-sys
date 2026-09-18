from sqlalchemy import create_engine, Column, String, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from rich.console import Console
from rich.table import Table
import datetime

engine = create_engine("sqlite:///StudentCourse.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
console = Console()

# Classes
class Student(Base):
    __tablename__ = "students"
    stuID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    level = Column(Integer)
    dept = Column(String)

    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )

class Course(Base):
    __tablename__ = "courses"
    courseID = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String, nullable=False)
    instructor = Column(String)

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan"
    )

class Enrollment(Base):
    __tablename__ = "enrollments"
    stuID = Column(Integer, ForeignKey("students.stuID"), primary_key=True)
    courseID = Column(Integer, ForeignKey("courses.courseID"), primary_key=True)
    date_enrolled = Column(Date)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    __table_args__ = (UniqueConstraint("stuID", "courseID", name="unique_enrollment"),)

Base.metadata.create_all(engine)

def validate_text(prompt, min_length=2):
    while True:
        value = input(prompt)
        if len(value.strip()) < min_length:
            console.print(f"Input must be at least {min_length} characters long. Try again!!!", style="bold bright_red")
            continue
        invalid_chars = "1234567890@#$%^&*()+=-_?!"
        if any(char in invalid_chars for char in value):
            console.print("Invalid input! Please enter a string. Try again!!!", style="bold bright_red")
        else:
            return value.strip()

def validate_level(prompt, min_level=1, max_level=5):
    while True:
        value = input(prompt)
        try:
            level = int(value)
            if level < min_level or level > max_level:
                console.print(f"Level must be between {min_level} and {max_level}. Try again!!!", style="bold bright_red")
            else:
                return level
        except ValueError:
            console.print("Invalid input! Level must be a number. Try again!!!", style="bold bright_red")

def confirm_action(prompt:str) -> bool :
    return input(f"{prompt} (Y/N) ").strip().lower() == 'y'


# Students 
def add_student():
    name ,level ,dept = validate_text("Name: ") ,validate_level("Level: ") ,validate_text("Dept: ")
    student = Student(name=name, level=level, dept=dept)
    session.add(student)
    session.commit()
    console.print(f"Student added successfully with ID {student.stuID}!", style="bold spring_green4")

def list_students():
    students = session.query(Student).all()
    table = Table(title="Students")
    table.add_column("ID", style="deep_pink4")
    table.add_column("Name", style="medium_orchid3")
    table.add_column("Level", style="magenta")
    table.add_column("Dept", style="plum4")
    for s in students:
        table.add_row(str(s.stuID), s.name, str(s.level), s.dept)
    console.print(table)

def update_student():
    while True:
        stuID = input("Enter Student ID to update (or 'exit' to return to menu): ")
        if stuID.lower() == "exit":
            return
        student = session.query(Student).filter_by(stuID=stuID).first()
        if not student:
            console.print("No student found with this ID!", style="bold bright_red")
            continue
        console.print("1. Name\n2. Level\n3. Department", style="magenta3", highlight=False)
        choice = input("Enter choice: ")
        if choice == "1":
            student.name = validate_text("New Name: ")
        elif choice == "2":
            student.level = validate_level("New Level: ")
        elif choice == "3":
            student.dept = validate_text("New Dept: ")
        else:
            console.print("Invalid choice!", style="bold bright_red")
            continue
        session.commit()
        console.print("Student updated successfully!", style="bold spring_green4")
        break

def delete_student():
    stuID = input("Enter Student ID to delete: ")
    student = session.query(Student).filter_by(stuID=stuID).first()
    if not student:
        console.print("No student found with this ID!", style="bold bright_red")
        return
    if confirm_action(f"Are you sure you want to delete student with ID {stuID}?") :
        session.delete(student)
        session.commit()
        console.print("Student deleted successfully!", style="bold spring_green4")

# Courses 
def add_course():
    cname ,instr = validate_text("Course Name: ") ,validate_text("Instructor: ")
    course = Course(course_name=cname, instructor=instr)
    session.add(course)
    session.commit()
    console.print(f"Course added successfully with ID {course.courseID}!", style="bold spring_green4")

def list_courses():
    courses = session.query(Course).all()
    table = Table(title="Courses")
    table.add_column("Course ID", style="grey63")
    table.add_column("Course Name", style="medium_orchid3")
    table.add_column("Instructor", style="medium_purple3")
    for c in courses:
        table.add_row(str(c.courseID), c.course_name, c.instructor)
    console.print(table)

def update_course():
    while True:
        courseID = input("Enter Course ID to update (or 'exit' to return to menu): ")
        if courseID.lower() == "exit":
            return
        course = session.query(Course).filter_by(courseID=courseID).first()
        if not course:
            console.print("No course found with this ID!", style="bold dark_red")
            continue
        console.print("1. Course Name\n2. Instructor", style="magenta3", highlight=False)
        choice = input("Enter choice: ")
        if choice == "1":
            course.course_name = validate_text("New Course Name: ")
        elif choice == "2":
            course.instructor = validate_text("New Instructor: ")
        else:
            console.print("Invalid choice!", style="bold bright_red")
            continue
        session.commit()
        console.print("Course updated successfully!", style="bold spring_green4")
        break

def delete_course():
    courseID = input("Enter Course ID to delete: ")
    course = session.query(Course).filter_by(courseID=courseID).first()
    if not course:
        console.print("No course found with this ID!", style="bold bright_red")
        return
    if confirm_action(f"Are you sure you want to delete course with ID {courseID}?") :
        session.delete(course)
        session.commit()
        console.print("Course deleted successfully!", style="bold spring_green4")

# Enrollments 
def enroll_student():
    sid ,cid = input("Student ID: ") ,input("Course ID: ")
    student = session.query(Student).filter_by(stuID=sid).first()
    course = session.query(Course).filter_by(courseID=cid).first()
    if not student or not course:
        console.print("Invalid Student or Course ID!", style="bold bright_red")
        return
    if session.query(Enrollment).filter_by(stuID=sid, courseID=cid).first():
        console.print("Student already enrolled in this course!", style="bold bright_red")
        return
    enrollment = Enrollment(stuID=sid, courseID=cid, date_enrolled=datetime.date.today())
    session.add(enrollment)
    session.commit()
    console.print(f"Student {sid} enrolled in {cid}!", style="bold spring_green4")

def list_enrollments():
    enrollments = session.query(Enrollment).all()
    table = Table(title="Enrollments")
    table.add_column("Student ID", style="deep_pink4")
    table.add_column("Course ID", style="grey63")
    table.add_column("Date Enrolled", style="pink3")
    for e in enrollments:
        table.add_row(str(e.stuID), str(e.courseID), str(e.date_enrolled))
    console.print(table)

def delete_enrollment():
    sid = input("Student ID: ")
    cid = input("Course ID: ")
    enrollment = session.query(Enrollment).filter_by(stuID=sid, courseID=cid).first()
    if not enrollment:
        console.print("No enrollment found with this Student ID and Course ID!", style="bold bright_red")
        return
    if confirm_action("Are you sure you want to delete this enrollment?") :
        session.delete(enrollment)
        session.commit()
        console.print("Enrollment deleted successfully!", style="bold spring_green4")
           
def menu():
    options = {
        "1" : add_student,
        "2" : list_students,
        "3" : update_student,
        "4" : delete_student,
        "5" : add_course,
        "6" : list_courses,
        "7" : update_course,
        "8" : delete_course,
        "9" : enroll_student,
        "10" : list_enrollments,
        "11" : delete_enrollment
    }
    while True:
        console.print("\n--------------------------- Student Course System ---------------------------", style="bold grey0 on white")
        console.print("1. Add Student\n2. List Students\n3. Update Student\n4. Delete Student\n5. Add Course\n6. List Courses\n7. Update Course\n8. Delete Course\n9. Enroll Student\n10. List Enrollments\n11. Delete Enrollment\n12. Exit", style="magenta" , highlight=False)

        choice = input("Enter choice: ")
        if choice == "12":
            console.print("Exiting program ^_^ ", style="bold deep_sky_blue4")
            break
        option = options.get(choice)
        if option :
            option()
        else :
            console.print("Invalid choice! Please enter a number between 1 and 12.", style="bold bright_red")

menu()

