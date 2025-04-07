from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="frontend")

# Sample results data
sample_results = {
    "12345": {"math": 85, "science": 78, "english": 92, "history": 70},
    "23456": {"math": 75, "science": 68, "english": 80, "history": 65},
}

@router.get("/", response_class=HTMLResponse)
def get_results(student_id: str, request: Request):
    if student_id not in sample_results:
        raise HTTPException(status_code=404, detail="Not Found")

    return templates.TemplateResponse("results.html", {
        "request": request,
        "student_id": student_id,
        "results": sample_results[student_id]
    })
