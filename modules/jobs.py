# -----------------------------
# modules/jobs.py
# -----------------------------

import json
import requests
from pathlib import Path

CONFIG_FILE = Path("company_config.json")

def load_company_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("companies", [])
    return []

def find_remote_jobs(keywords):
    query = "+".join(keywords)
    url = f"https://remotive.io/api/remote-jobs?search={query}"
    try:
        response = requests.get(url)
        data = response.json()
        jobs = [
            {
                "title": job["title"],
                "company": job["company_name"],
                "url": job["url"]
            }
            for job in data.get("jobs", [])
        ]
        return jobs
    except Exception as e:
        print(f"Error fetching remote jobs: {e}")
        return []

def search_career_pages():
    companies = load_company_config()
    # Placeholder logic — simulate a job from each company
    return [
        {
            "title": f"Job at {company['name']}",
            "company": company["name"],
            "url": company["url"]
        }
        for company in companies
    ]

def filter_jobs_by_keywords(jobs, keywords):
    filtered = []
    for job in jobs:
        if any(kw.lower() in job["title"].lower() for kw in keywords):
            filtered.append(job)
    return filtered
