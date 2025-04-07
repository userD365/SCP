from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter
import httpx
import uvicorn

# Import route modules
from backend.routes import auth_routes, result_routes, feedback_routes

app = FastAPI()

# Mount static directory (for CSS/JS/images if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates directory
templates = Jinja2Templates(directory="frontend")

# Register routers
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(result_routes.router, prefix="/results")
app.include_router(feedback_routes.router, prefix="/feedback")

# Serve login page at /
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 🆕 Fetch external results from friend's API
@app.get("/external-results/{student_id}", response_class=HTMLResponse)
async def get_external_results(student_id: str, request: Request):
    api_url = f"http://scp-exam-app-env.eba-3hfvxmq4.us-east-1.elasticbeanstalk.com/api/results/{student_id}/"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)

    if response.status_code == 200:
        result_data = response.json()
        return templates.TemplateResponse("results.html", {"request": request, "results": result_data})
    else:
        return templates.TemplateResponse("results.html", {"request": request, "results": None, "error": "Failed to fetch results."})


# Run with: python backend/main.py
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
