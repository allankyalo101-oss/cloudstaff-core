#!/bin/bash
# ================================================
# CloudStaff Local Repo Cleanup Script
# ================================================
# Purpose:
# 1. Keep only main repo 'cloudstaff-core'
# 2. Ensure correct remote
# 3. Optionally remove local backup folders
# ================================================

# Set variables
MAIN_REPO="$HOME/cloudstaff-core"
BACKUP_REPO="$HOME/cloudstaff-core_BACKUP"
ENV_BACKUP="$HOME/cloudstaff-core-env-backup"
REMOTE_URL="https://github.com/allankyalo101-oss/cloudstaff-core.git"

echo "=== Starting CloudStaff repo cleanup ==="

# Step 1: Verify main repo exists
if [ ! -d "$MAIN_REPO/.git" ]; then
    echo "[ERROR] Main repo not found at $MAIN_REPO"
    exit 1
fi
echo "[OK] Found main repo at $MAIN_REPO"

# Step 2: Ensure main repo remote is correct
cd "$MAIN_REPO"
git remote remove origin 2>/dev/null
git remote add origin "$REMOTE_URL"
echo "[OK] Remote set to $REMOTE_URL"

# Step 3: Optional - Remove local backup folder (uncomment if you want)
# rm -rf "$BACKUP_REPO"
# echo "[INFO] Removed backup repo folder $BACKUP_REPO"

# rm -rf "$ENV_BACKUP"
# echo "[INFO] Removed .env backup folder $ENV_BACKUP"

# Step 4: List current repos in home directory for verification
echo "=== Remaining CloudStaff folders in home directory ==="
ls -d ~/cloudstaff* 2>/dev/null

echo "=== Cleanup complete. Main repo ready at $MAIN_REPO ==="
echo "To push changes, use: git push origin master"

