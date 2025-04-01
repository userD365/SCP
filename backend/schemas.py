from pydantic import BaseModel

class StudentLogin(BaseModel):
    student_id: str
    password: str

class FeedbackCreate(BaseModel):
    student_id: str
    feedback_text: str
