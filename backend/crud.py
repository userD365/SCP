from sqlalchemy.orm import Session
from backend import models, schemas

# Function to create/register a new student (optional if you skip registration)
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Function to authenticate student (just gets record by student_id)
def authenticate_student(db: Session, student_id: str):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()
