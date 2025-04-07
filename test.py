# Step 1: Import your DB setup
from backend.database import SessionLocal
from backend import models

# Step 2: Open DB session
db = SessionLocal()

# Step 3: Query all students
students = db.query(models.Student).all()
for student in students:
    print(student.student_id, student.name)

# Optional: See feedback too
feedbacks = db.query(models.Feedback).all()
for fb in feedbacks:
    print(fb.student_id, fb.feedback_text)


# Step 4: Close DB session
db.close()
