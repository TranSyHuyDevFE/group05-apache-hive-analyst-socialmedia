#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
GITHUB_USERNAME="khaphan-github" # Replace with your GitHub username
GITHUB_EMAIL="phanhoangkha01@gmail.com" # Replace with your GitHub email
REPO_URL="https://github.com/TranSyHuyDevFE/group05-apache-hive-analyst-socialmedia.git" # Replace with your repository URL
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FOLDER_A="$SCRIPT_DIR/raw_data/tiktok_zipped" # Replace with the source folder
FOLDER_B="$SCRIPT_DIR/group05-apache-hive-analyst-socialmedia/crawler/raw_data/tiktok_zipped" # Replace with the destination folder
BRANCH_NAME="tiktok_crawler_data" # Replace with the branch name you want to create

# Configure Git
git config --global user.name "$GITHUB_USERNAME"
git config --global user.email "$GITHUB_EMAIL"

# Clone the repository only if the folder does not exist
REPO_NAME=$(basename "$REPO_URL" .git)
if [ ! -d "$SCRIPT_DIR/$REPO_NAME" ]; then
    git clone "$REPO_URL" "$SCRIPT_DIR/$REPO_NAME"
fi
cd "$SCRIPT_DIR/$REPO_NAME"

# Create and switch to a new branch only if not already on it
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
    git checkout "$BRANCH_NAME"
fi

# Ensure folder B exists
mkdir -p "$FOLDER_B"

# Move files from folder A to folder B
if [ "$(ls -A "$FOLDER_A" 2>/dev/null)" ]; then
    mv "$FOLDER_A"/* "$FOLDER_B"/
fi

# Stage changes, commit, and push
# Use the correct relative path for git add
git add crawler/raw_data/tiktok_zipped
COMMIT_MESSAGE="crawldata $(date +'%Y-%m-%d %H:%M')"
git commit -m "$COMMIT_MESSAGE"
git push -u origin "$BRANCH_NAME"