Step 1: Verify Local Directory Structure
Ensure the local project folder contains the exact file hierarchy below before initializing Git:

predictive-maintenance-mlops/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions CI/CD pipeline
├── app.py                          # Streamlit application
├── Dockerfile                      # Container build instructions
├── requirements.txt                # Python dependencies
├── xgboost_model.pkl               # Serialized model artifact
└── README.md                       # Project documentation

Verification points:

Ensure .github/workflows/deploy.yml has the correct path (notice the leading dot on .github).

In deploy.yml, verify that YOUR_HF_USERNAME and YOUR_SPACE_NAME are replaced with your actual Hugging Face username and destination Space name.

Step 2: Create a Docker Space on Hugging Face
Hugging Face Spaces will serve as the cloud runtime executing your containerized Streamlit application.

Navigate to Hugging Face and log in.

In the top-right profile menu, click New Space.

Configure the Space settings:

Space Name: predictive-maintenance-dashboard (or your preferred name).

License: mit or apache-2.0.

Select the Space SDK: Choose Docker (select the Blank template; do not select the native Streamlit SDK, as the rubric mandates a custom Dockerfile).

Space Hardware: Free (CPU basic · 2 vCPU · 16 GB).

Visibility: Public (required for university evaluation).

Click Create Space.

Keep this tab open to monitor the build once code is pushed.

Step 3: Set Up the GitHub Repository & Add Secret
GitHub will host the source code and trigger the automated CI/CD pipeline.

Go to GitHub and create a new repository:

Repository name: predictive-maintenance-mlops

Visibility: Public

Do not initialize with a README, .gitignore, or license (you already have these locally).

Configure your Hugging Face authentication secret:

In your new GitHub repository, click Settings (top menu bar).

In the left sidebar, navigate to Secrets and variables > Actions.

Click New repository secret.

Name: HF_TOKEN

Secret: Paste your Hugging Face Write Token (found under HF Settings > Access Tokens).

Click Add secret.

Step 4: Initialize Git and Push to GitHub
Open a terminal (or command prompt) in your project root directory and execute the following sequence:

Bash
# Initialize local git repository
git init

# Stage all files including hidden workflow directories
git add .

# Commit project files
git commit -m "feat: complete predictive maintenance deployment pipeline"

# Set branch to main
git branch -M main

# Link to your remote GitHub repository (replace with your actual GitHub URL)
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/predictive-maintenance-mlops.git

# Push to GitHub
git push -u origin main
Step 5: Monitor the CI/CD Pipeline & Validate Deployment
Inspect GitHub Actions:

Go to the Actions tab in your GitHub repository.

You will see the workflow Sync to Hugging Face Hub running.

Click into the run to view the execution logs until all steps complete with a green checkmark.

Inspect Hugging Face Build:

Navigate to your Hugging Face Space page.

The Space status will transition from Building (pulling Debian base, installing system packages, running pip install -r requirements.txt) to Running.

Once live, interact with the dashboard: adjust slider values (e.g., set Engine_rpm to 1200 and Lub_oil_pressure to 1.5) and verify that the model returns an immediate Active Failure Imminent (High Risk) alert.