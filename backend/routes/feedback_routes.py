from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import crud, schemas

router = APIRouter()
templates = Jinja2Templates(directory="frontend")

# GET: Show feedback form
@router.get("/", response_class=HTMLResponse)
def show_feedback_form(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request})

# POST: Handle feedback form submission
@router.post("/")
def submit_feedback(
    student_id: str = Form(...),
    feedback_text: str = Form(...),
    db: Session = Depends(get_db)
):
    feedback_data = schemas.FeedbackCreate(student_id=student_id, feedback_text=feedback_text)
    crud.create_feedback(db, feedback_data)
    return RedirectResponse(url="/feedback/", status_code=303)
