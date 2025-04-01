from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

# Student Model: Stores student data
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    student_id = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<Student(id={self.id}, student_id='{self.student_id}')>"

# Feedback Model: Stores feedback given by students
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, nullable=False)
    feedback_text = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Feedback(id={self.id}, student_id='{self.student_id}')>"
