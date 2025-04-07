from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

router = APIRouter()
templates = Jinja2Templates(directory="frontend")

EXTERNAL_API_URL = "http://scp-exam-app-env.eba-3hfvxmq4.us-east-1.elasticbeanstalk.com/api/results"

@router.get("/", response_class=HTMLResponse)
async def get_results(student_id: str, request: Request):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{EXTERNAL_API_URL}/{student_id}/")
            response.raise_for_status()
            results = response.json()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Student results not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return templates.TemplateResponse("results.html", {
        "request": request,
        "student_id": student_id,
        "results": results
    })
