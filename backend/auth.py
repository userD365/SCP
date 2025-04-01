from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models

router = APIRouter()
templates = Jinja2Templates(directory="frontend")

# Unified login/register page (GET)
@router.get("/login", response_class=HTMLResponse)
@router.get("/register", response_class=HTMLResponse)
def show_login_register_form(request: Request):
    return templates.TemplateResponse("login_register.html", {"request": request})

# Registration handler (POST)
@router.post("/register")
def register_user(
    name: str = Form(...),
    student_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check for duplicate student_id
    existing_student = db.query(models.Student).filter_by(student_id=student_id).first()
    if existing_student:
        return HTMLResponse(
            content=f"<h3>Student ID '{student_id}' already exists. Try logging in.</h3>",
            status_code=400
        )

    # Create new student record
    new_student = models.Student(
        name=name.strip(),
        student_id=student_id.strip(),
        password=password
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    # Redirect back to login form
    return RedirectResponse(url="/auth/login", status_code=303)
