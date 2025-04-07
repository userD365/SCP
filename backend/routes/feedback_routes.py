from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models

router = APIRouter()
templates = Jinja2Templates(directory="frontend")

# ✅ GET: Show feedback form
@router.get("/", response_class=HTMLResponse)
def show_feedback_form(request: Request, student_id: str = ""):
    return templates.TemplateResponse("feedback.html", {
        "request": request,
        "student_id": student_id
    })

# ✅ POST: Submit new feedback
@router.post("/")
def submit_feedback(
    student_id: str = Form(...),
    feedback_text: str = Form(...),
    db: Session = Depends(get_db)
):
    new_feedback = models.Feedback(student_id=student_id, feedback_text=feedback_text)
    db.add(new_feedback)
    db.commit()
    return RedirectResponse(url=f"/feedback/view?student_id={student_id}", status_code=303)

# ✅ GET: View feedbacks for a student (HTML view)
@router.get("/view", response_class=HTMLResponse)
def view_feedbacks(request: Request, student_id: str, db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).filter(models.Feedback.student_id == student_id).all()
    return templates.TemplateResponse("view_feedback.html", {
        "request": request,
        "student_id": student_id,
        "feedbacks": feedbacks
    })

# ✅ GET: View feedbacks via JSON API (external use)
@router.get("/api/view", response_class=JSONResponse)
def view_feedbacks_api(student_id: str, db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).filter(models.Feedback.student_id == student_id).all()
    if not feedbacks:
        return JSONResponse(content={"message": "No feedbacks found"}, status_code=404)

    result = [
        {
            "id": fb.id,
            "student_id": fb.student_id,
            "feedback_text": fb.feedback_text
        }
        for fb in feedbacks
    ]
    return JSONResponse(content=result)

# ✅ GET: Edit feedback form
@router.get("/edit/{feedback_id}", response_class=HTMLResponse)
def edit_feedback_form(request: Request, feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return templates.TemplateResponse("edit_feedback.html", {
        "request": request,
        "feedback": feedback
    })

# ✅ POST: Update feedback
@router.post("/edit/{feedback_id}")
def update_feedback(
    feedback_id: int,
    student_id: str = Form(...),
    feedback_text: str = Form(...),
    db: Session = Depends(get_db)
):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    feedback.feedback_text = feedback_text
    db.commit()
    return RedirectResponse(url=f"/feedback/view?student_id={student_id}", status_code=303)

# ✅ GET: Delete feedback
@router.get("/delete/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    student_id = feedback.student_id
    db.delete(feedback)
    db.commit()
    return RedirectResponse(url=f"/feedback/view?student_id={student_id}", status_code=303)
