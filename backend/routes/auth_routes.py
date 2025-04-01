from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import schemas, models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(data: schemas.StudentLogin, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter_by(student_id=data.student_id, password=data.password).first()
    if not student:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "student_id": student.student_id}
