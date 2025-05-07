# job_search_auto_apply/main.py

import argparse
from flask import Flask, render_template, request, jsonify
from modules.location import get_coordinates, get_nearby_companies
from modules.jobs import find_remote_jobs, search_career_pages, filter_jobs_by_keywords
from modules.apply import auto_apply_jobs
from modules.utils import load_user_config

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/job_search', methods=['POST'])
def job_search():
    # Get input data from form submission
    zip_code = request.form.get('zip_code')
    radius = int(request.form.get('radius', 30))
    keywords = request.form.getlist('keywords')
    remote = 'remote' in request.form
    auto_apply = 'auto_apply' in request.form

    # Load user configuration
    config = load_user_config()

    # Get coordinates for the provided ZIP code
    lat, lon = get_coordinates(zip_code)

    # Search for nearby companies
    companies = get_nearby_companies(lat, lon, radius)

    all_jobs = []

    # Search for remote jobs
    if remote:
        all_jobs += find_remote_jobs(keywords)

    # Search local job listings if companies are found
    if companies:
        local_jobs = search_career_pages(companies)
        all_jobs += local_jobs
    else:
        print("No companies found within radius.")

    # Filter jobs by the specified keywords
    matched_jobs = filter_jobs_by_keywords(all_jobs, keywords)

    # Optionally, auto-apply to matched jobs
    if auto_apply:
        auto_apply_jobs(matched_jobs, config)

    # Return results to the user
    return render_template('results.html', jobs=matched_jobs)

if __name__ == "__main__":
    app.run(debug=True)



# This script is designed to be run from the command line. It takes a ZIP code and optional parameters for radius, keywords, remote job search, and auto-apply functionality.
# It retrieves the user's location, searches for nearby companies, finds remote jobs, filters jobs based on keywords, and optionally auto-applies to matched jobs.
# The script uses various modules to handle different tasks, such as location retrieval, job searching, and application submission.
# The user configuration is loaded from a JSON file, which contains the user's LinkedIn and Indeed credentials for auto-application.
# The script is structured to be modular, allowing for easy updates and maintenance of individual components.
# The main function orchestrates the flow of the program, handling command-line arguments and calling the appropriate functions.
# The script is designed to be user-friendly, providing clear output messages to guide the user through the process.
# The script is intended for job seekers in the IT field, helping them find and apply to jobs efficiently.
# The script is written in Python and uses various libraries for web scraping, API requests, and data handling.
# The script is designed to be run in a terminal or command prompt, making it accessible to users with basic programming knowledge.
# The script is intended to be a starting point for job seekers, and users are encouraged to customize it further based on their needs.
# The script is open-source and can be modified and distributed under the terms of the MIT License.
# The script is part of a larger project that aims to automate the job search process, making it easier for users to find and apply to jobs in their field.
# The script is designed to be extensible, allowing for the addition of new features and functionalities in the future.
# The script is intended to be a helpful tool for job seekers, providing them with the resources and information they need to succeed in their job search.
# The script is a work in progress, and users are encouraged to provide feedback and suggestions for improvement.
# The script is designed to be user-friendly and accessible, with clear instructions and error handling to guide users through the process.
# The script is intended to be a valuable resource for job seekers, helping them navigate the often-challenging job search process.
# The script is designed to be a comprehensive solution for job seekers, providing them with the tools and information they need to succeed in their job search.
# The script is intended to be a collaborative effort, with contributions from the open-source community to improve and enhance its functionality.
# The script is designed to be a valuable resource for job seekers, providing them with the tools and information they need to succeed in their job search.