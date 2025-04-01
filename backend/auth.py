from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.context import CryptContext  # For password hashing
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.crud import authenticate_student

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Verify password using bcrypt hashing
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# GET route to show login form
@router.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# POST route to handle login logic
@router.post("/login")
def login_user(
    student_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    request: Request = None  # Optional for handling flash messages or session
):
    student = authenticate_student(db, student_id)  # Get student by ID

    if not student:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify if the provided password matches the hashed password stored in the DB
    if not verify_password(password, student.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # If authentication is successful, redirect to the results page
    return RedirectResponse(url=f"/results?student_id={student_id}", status_code=303)
