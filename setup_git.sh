#!/bin/bash
# ==========================================
# Script: setup_git.sh
# Purpose: Prepare cloudstaff-core for GitHub
# Actions:
#   - Remove __pycache__ directories
#   - Create .gitignore for venv, caches, and logs
#   - Initialize Git repository
#   - Commit files
#   - Add remote and push to GitHub
# ==========================================

# --- Step 1: Clean __pycache__ directories ---
echo "Cleaning up __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} +
echo "__pycache__ cleanup complete."

# --- Step 2: Create .gitignore ---
echo "Creating .gitignore..."
cat > .gitignore <<EOL
# Python cache
**/__pycache__/
**/*.py[cod]

# Virtual environment
venv/

# Optional runtime logs
cloudstaff_core/logs/
EOL
echo ".gitignore created."

# --- Step 3: Initialize Git repository ---
echo "Initializing Git repository..."
git init
git add .
git commit -m "Initial commit of cloudstaff-core"
echo "Git repository initialized and initial commit made."

# --- Step 4: Add remote and push to GitHub ---
# NOTE: Replace <YOUR_GITHUB_REPO_URL> with your actual GitHub repo URL
GITHUB_REPO_URL="<YOUR_GITHUB_REPO_URL>"

if [ "$GITHUB_REPO_URL" != "<YOUR_GITHUB_REPO_URL>" ]; then
    git remote add origin "$GITHUB_REPO_URL"
    git branch -M main
    git push -u origin main
    echo "Code pushed to GitHub repository at $GITHUB_REPO_URL"
else
    echo "Please edit the script to set your GitHub repository URL in the GITHUB_REPO_URL variable."
fi

echo "Setup complete."
