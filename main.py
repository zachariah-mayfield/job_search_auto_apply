# job_search_auto_apply/main.py

# -----------------------------
# main.py
# -----------------------------



from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

CONFIG_PATH = os.path.join("config", "company_config.json")

def load_companies():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f).get("companies", [])
    return []

def save_companies(companies):
    sorted_companies = sorted(companies, key=lambda x: x["name"].lower())
    with open(CONFIG_PATH, "w") as f:
        json.dump({"companies": sorted_companies}, f, indent=4)

@app.route("/edit_companies", methods=["GET", "POST"])
def edit_companies():
    if request.method == "POST":
        name = request.form.get("companyName")
        url = request.form.get("careerUrl")

        companies = load_companies()
        if not any(c["name"].lower() == name.lower() for c in companies):
            companies.append({"name": name, "career_url": url})
            save_companies(companies)

        return redirect("/edit_companies")

    companies = load_companies()
    return render_template("company_editor.html", companies=companies)


@app.route("/delete_company", methods=["POST"])
def delete_company():
    name = request.form.get("companyName")
    companies = load_companies()
    companies = [c for c in companies if c["name"].lower() != name.lower()]
    save_companies(companies)
    return redirect("/edit_companies")


@app.route("/edit_company", methods=["POST"])
def edit_company():
    old_name = request.form.get("oldName")
    new_name = request.form.get("newName")
    new_url = request.form.get("newUrl")

    companies = load_companies()
    for company in companies:
        if company["name"].lower() == old_name.lower():
            company["name"] = new_name
            company["career_url"] = new_url
            break

    save_companies(companies)
    return redirect("/edit_companies")


@app.route("/job_search", methods=["GET", "POST"])
def job_search():
    if request.method == "POST":
        keyword = request.form["keyword"]
        location = request.form.get("location", "")  # Default to empty if location is not provided
        jobs = search_jobs(keyword, location)
        return render_template("job_search.html", jobs=jobs)
    return render_template("job_search.html", jobs=[])


def search_jobs(keyword, location):
    # Mock job data to simulate real-world job listings
    jobs = [
        {"title": "Software Engineer - Ansible", "company": "Google", "location": "Remote", "url": "https://careers.google.com/jobs/results/"},
        {"title": "DevOps Engineer with Ansible", "company": "Amazon", "location": "Remote", "url": "https://www.amazon.jobs/en/jobs/123456"},
        {"title": "Data Scientist", "company": "Facebook", "location": "Remote", "url": "https://www.facebook.com/careers/jobs/789012"},
        {"title": "Cloud Engineer - Ansible and Kubernetes", "company": "Microsoft", "location": "Remote", "url": "https://careers.microsoft.com/jobs/987654"},
    ]

    # Perform a case-insensitive search for the keyword
    if keyword:
        jobs = [job for job in jobs if keyword.lower() in job["title"].lower()]
    
    # Filter jobs by location if provided
    if location:
        jobs = [job for job in jobs if location.lower() in job["location"].lower()]
    
    return jobs


if __name__ == "__main__":
    app.run(debug=True)
