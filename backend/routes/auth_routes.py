from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.crud import authenticate_student

router = APIRouter()
templates = Jinja2Templates(directory="frontend")

# GET: Show login form
@router.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# POST: Handle login
@router.post("/login")
def login_user(
    student_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    request: Request = None
):
    # Get student by student_id
    student = authenticate_student(db, student_id)

    if not student:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Compare plain-text password
    if password != student.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Successful login — redirect to results page
    return RedirectResponse(url=f"/results?student_id={student_id}", status_code=303)
