title: Proactive Asset Health Dashboard 
emoji: ⚙️ 
colorFrom: blue colorTo: green 
sdk: docker 
app_port: 7860 
pinned: false
—
Predictive Maintenance MLOps Pipeline: Execution & CI/CD Guide (Colab Edition)
This guide provides the exact step-by-step instructions to train your Machine Learning model in Google Colab, and deploy the interactive dashboard to Hugging Face via GitHub Actions (CI/CD).
Phase 1: Model Training & Artifact Generation
Environment: Google Colab Notebook
Since Colab resets every time you close it, you need to generate your model artifact (.pkl) and download all necessary files to your local computer before moving to GitHub.
Step 1: Install Dependencies in Colab
In a new Colab cell, run:
!pip install pandas scikit-learn xgboost mlflow streamlit joblib datasets huggingface_hub



Step 2: Create the Training Script
Copy the code from your train.py file into a Colab cell and execute it.
Alternatively, write it to the Colab disk by running this in a cell:
# Write the train.py code into the cell, starting with:
%%writefile train.py
import os
import pandas as pd
# ... (rest of train.py code) ...



Run the script in the next cell:
!python train.py



(Verify: You should see metrics printed and "Champion model successfully saved to xgboost_model.pkl").
Step 3: Download Your Files
You now need to download the following 5 files from the Colab file explorer (folder icon on the left sidebar) to your local computer:
train.py
xgboost_model.pkl (Generated in Step 2)
app.py (Create this in Colab using %%writefile app.py or download from your IDE)
requirements.txt
Dockerfile
Phase 2: Hugging Face Setup
Environment: Web Browser (huggingface.co)
Step 1: Create the Host Space
Go to Hugging Face Spaces and click Create new Space.
Space Name: Predictive-Maintenance-App (or your preferred name).
License: Openrail (or your choice).
Select the Space SDK: Choose Docker (Blank).
Space Hardware: Free (CPU).
Click Create Space.
Step 2: Generate an Access Token
Go to your Hugging Face Profile Settings -> Access Tokens (https://huggingface.co/settings/tokens).
Click New Token.
Name it GITHUB_ACTIONS_TOKEN.
Role: Select Write.
Click Generate and copy this token to your clipboard.
Phase 3: GitHub CI/CD Automation
Environment: Web Browser (github.com)
Step 1: Create the GitHub Repository
Go to GitHub and create a new repository (e.g., predictive-maintenance-capstone).
Important: Initialize it by checking the box "Add a README file". (This makes it easier to upload files via the browser).
Step 2: Add the Hugging Face Token to GitHub Secrets
In your new GitHub repository, go to Settings (top tab) -> Secrets and variables (left sidebar) -> Actions.
Click New repository secret (green button).
Name: HF_TOKEN
Secret: Paste the token you copied from Hugging Face in Phase 2.
Click Add secret.
Step 3: Upload Project Files
Go back to your repository's main <> Code tab.
Click Add file -> Upload files.
Drag and drop the 5 files you downloaded from Colab:
app.py
train.py
xgboost_model.pkl
requirements.txt
Dockerfile
Click Commit changes.
Step 4: Create the CI/CD Pipeline File
We now tell GitHub to automatically send these files to Hugging Face.
In your repository, click Add file -> Create new file.
In the file name box, type exactly this: .github/workflows/deploy.yml (This will automatically create the hidden folders).
Paste the following YAML code into the editor:
name: Sync to Hugging Face Hub

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  sync-to-hub:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          lfs: true
      
      - name: Push to Hugging Face Spaces
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git config --global user.email "actions@github.com"
          git config --global user.name "GitHub Actions CI/CD"
          # IMPORTANT: Replace YOUR_HF_USERNAME below with your actual Hugging Face username!
          git push --force https://YOUR_HF_USERNAME:$HF_TOKEN@huggingface.co/spaces/YOUR_HF_USERNAME/Predictive-Maintenance-App main



CRITICAL: Change YOUR_HF_USERNAME on the very last line to your actual Hugging Face username.
Click Commit changes.
Phase 4: Verify Deployment
Environment: Web Browser
As soon as you commit the deploy.yml file, GitHub Actions will trigger.
Go to your GitHub repository's Actions tab. You will see a yellow spinning circle indicating the build is running. Wait for it to turn into a green checkmark.
Go to your Hugging Face Space. The status at the top will change from "Building" to "Running".
Congratulations! Your predictive maintenance dashboard is now live on the cloud, and any future file changes you upload to GitHub will automatically trigger a new deployment.
