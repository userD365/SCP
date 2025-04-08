from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import os

router = APIRouter()
templates = Jinja2Templates(directory="frontend")

EXTERNAL_API_URL = "http://scp-exam-app-env.eba-3hfvxmq4.us-east-1.elasticbeanstalk.com/api/results"
TOKEN_URL = "http://scp-exam-app-env.eba-3hfvxmq4.us-east-1.elasticbeanstalk.com/api/token/"

# Use env vars or defaults for dev/testing
USERNAME = os.getenv("API_USERNAME", "admin1")
PASSWORD = os.getenv("API_PASSWORD", "123456")

async def get_jwt_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, json={
            "username": USERNAME,
            "password": PASSWORD
        })
        response.raise_for_status()
        return response.json().get("access")

@router.get("/", response_class=HTMLResponse)
async def get_results(student_id: str, request: Request):
    try:
        token = await get_jwt_token()
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{EXTERNAL_API_URL}/{student_id}/", headers=headers)
            response.raise_for_status()
            data = response.json()

        # Parse and structure results
        student_name = data.get("student_name", "Unknown")
        subjects = data.get("subjects", [])

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Student results not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return templates.TemplateResponse("results.html", {
        "request": request,
        "student_id": student_id,
        "student_name": student_name,
        "results": subjects
    })
