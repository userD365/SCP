from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    student_id: str
    password: str

    class Config:
        orm_mode = True  # To allow ORM mapping
