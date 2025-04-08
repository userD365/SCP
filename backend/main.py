from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
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


# ✅ Optional JWT token (if your friend's API is secured)
# USERNAME = os.getenv("API_USERNAME", "admin1")
# PASSWORD = os.getenv("API_PASSWORD", "123456")
# TOKEN_URL = "http://scp-exam-app-env.eba-3hfvxmq4.us-east-1.elasticbeanstalk.com/api/token/"

# async def get_token():
#     async with httpx.AsyncClient() as client:
#         response = await client.post(TOKEN_URL, json={"username": USERNAME, "password": PASSWORD})
#         response.raise_for_status()
#         return response.json().get("access")

# ✅ External results fetch
@app.get("/external-results/{student_id}", response_class=HTMLResponse)
async def get_external_results(student_id: str, request: Request):
    api_url = f"http://scp-exam-app-env.eba-3hfvxmq4.us-east-1.elasticbeanstalk.com/api/results/{student_id}/"

    try:
        async with httpx.AsyncClient() as client:
            # token = await get_token()
            # headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(api_url)  # , headers=headers if needed

        response.raise_for_status()
        result_data = response.json()
        return templates.TemplateResponse("results.html", {
            "request": request,
            "student_id": student_id,
            "results": result_data
        })
        
    except httpx.HTTPStatusError as e:
        return templates.TemplateResponse("results.html", {
            "request": request,
            "student_id": student_id,
            "results": None,
            "error": f"API Error: {e.response.status_code}"
        })
    except Exception as e:
        return templates.TemplateResponse("results.html", {
            "request": request,
            "student_id": student_id,
            "results": None,
            "error": f"Unexpected error: {str(e)}"
        })


# Run with: python backend/main.py
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
