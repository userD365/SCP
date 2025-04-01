import requests
from fastapi import APIRouter

router = APIRouter()

@router.get("/{student_id}")
def fetch_results(student_id: str):
    # Replace this URL with your real app’s endpoint
    external_api_url = f"http://localhost:8001/results/{student_id}"
    response = requests.get(external_api_url)
    return response.json()
