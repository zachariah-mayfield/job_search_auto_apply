# -----------------------------
# fastapi_app.py
# -----------------------------

from fastapi import FastAPI
from pydantic import BaseModel
from modules.jobs import find_remote_jobs, search_career_pages, filter_jobs_by_keywords
from modules.location import get_coordinates

app = FastAPI()

class JobSearchRequest(BaseModel):
    zip_code: str
    radius: int
    keywords: list
    remote: bool
    auto_apply: bool

@app.get("/")
async def read_root():
    return {"message": "Job Search Auto Apply"}

@app.post("/search_jobs")
async def search_jobs(request: JobSearchRequest):
    zip_code = request.zip_code
    radius = request.radius
    keywords = request.keywords
    remote = request.remote
    auto_apply = request.auto_apply
    
    # Get the coordinates for the zip code
    lat, lon = get_coordinates(zip_code)
    
    # Using Remotive API for remote jobs
    remote_jobs = find_remote_jobs(keywords)
    
    # Add manual company career page URLs
    companies = ['google', 'microsoft', 'amazon']  # Example, add more as needed
    career_page_jobs = search_career_pages(companies)
    
    # Combine remote jobs and career page jobs
    all_jobs = remote_jobs + career_page_jobs
    
    # Filter the jobs by keywords
    filtered_jobs = filter_jobs_by_keywords(all_jobs, keywords)
    
    return {"jobs": filtered_jobs}
