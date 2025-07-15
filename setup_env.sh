#!/bin/bash

# Ensure the script is being run from the project root
PROJECT_DIR="/z/Main/github-repos/job_search_auto_apply"

# Navigate to the project directory
cd "$PROJECT_DIR" || { echo "Project directory not found!"; exit 1; }

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating a virtual environment..."
  python -m venv venv
else
  echo "Virtual environment already exists. Skipping creation."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete! Virtual environment is ready."

flask run
