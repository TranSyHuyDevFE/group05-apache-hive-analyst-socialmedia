#!/usr/bin/env bash
set -e

# Configuration
SCRIPT_NAME=$(basename "$0")
TARGET_DIR_DATA="volumes/warehouse/tiktok"
TARGET_DIR_SCRIPT="volumes/warehouse"
SRC_DIR="cleaned_data"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print error messages
error_exit() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
    exit 1
}

# Function to print info messages
info() {
    echo -e "${GREEN}[INFO] $1${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if docker is running
if ! docker info >/dev/null 2>&1; then
    error_exit "Docker is not running. Please start Docker and try again."
fi

# Check if hiveserver2 container is running
if ! docker ps | grep -q hiveserver2; then
    error_exit "HiveServer2 container is not running. Please start the container and try again."
fi

# Check if source directory exists
if [ ! -d "$SRC_DIR" ]; then
    error_exit "Source directory '$SRC_DIR' does not exist. Please check the path and try again."
fi

# Step 1: Create folders in warehouse for each table
info "Creating directory structure in warehouse..."

# Using indexed arrays instead of associative arrays for better compatibility
tbl_names=("category" "comments" "related_videos" "video" "video_info_details" "user_info_details")
tbl_files=("category.csv" "comments.csv" "related_videos.csv" "video_info.csv" "video_info_details.csv" "user_info_details.csv")

# Create directories for each table
for tbl in "${tbl_names[@]}"; do
    mkdir -p "$TARGET_DIR_DATA/$tbl" || error_exit "Failed to create directory: $TARGET_DIR_DATA/$tbl"
done

info "Directory structure created successfully"

# Step 2: Copy each data file to its folder
info "Copying data files to warehouse..."

# Copy data files to their respective directories
for i in "${!tbl_names[@]}"; do
    tbl="${tbl_names[$i]}"
    src_path="$SRC_DIR/$tbl"
    if [ -d "$src_path" ] && [ "$(ls -A "$src_path" 2>/dev/null)" ]; then
        cp -r "$src_path"/. "$TARGET_DIR_DATA/$tbl/" || error_exit "Failed to copy data for table: $tbl"
    else
        echo -e "${YELLOW}[WARNING] No data found for table: $tbl${NC}"
    fi
done

info "Data files copied successfully"

# Step 3: Copy scripts folder to warehouse
info "Updating scripts in warehouse..."

if [ ! -d "scripts" ]; then
    error_exit "Scripts directory not found. Please run from the project root directory."
fi

rm -rf "$TARGET_DIR_SCRIPT/scripts" || error_exit "Failed to remove old scripts"
cp -r "scripts" "$TARGET_DIR_SCRIPT/" || error_exit "Failed to copy scripts to warehouse"

info "Scripts updated successfully"

# Step 4: Execute Hive scripts
info "Executing Hive scripts..."

# Check if script files exist in container
if ! docker exec hiveserver2 [ -f "/opt/hive/data/warehouse/scripts/remove-db-structure.hql" ]; then
    error_exit "Hive script remove-db-structure.hql not found in container"
fi

# Remove existing database structure
info "Removing existing database structure..."
if ! docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/remove-db-structure.hql; then
    echo -e "${YELLOW}[WARNING] Failed to remove database structure. Continuing anyway...${NC}"
fi

# Create tables
info "Creating tables..."
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/create-tables.hql || \
    error_exit "Failed to create tables"

# Create views
info "Creating views..."
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/create-views.hql || \
    error_exit "Failed to create views"

info "Hive scripts executed successfully"

# Step 5: Test sentiment analysis setup
info "Testing sentiment analysis setup..."

info "Counting comments with sentiment analysis..."
docker exec -i hiveserver2 beeline --silent=true --outputformat=tsv2 -u jdbc:hive2://localhost:10000 -e "
    SELECT 'Comments with sentiment analysis:' as description, 
           COUNT(*) as total_comments 
    FROM tiktok_comments 
    WHERE sentiment IS NOT NULL;" 2>/dev/null | grep -v '^+' | grep -v 'rows selected'

info "Sentiment summary dashboard preview:"
docker exec -i hiveserver2 beeline --silent=true --outputformat=tsv2 -u jdbc:hive2://localhost:10000 -e "
    SELECT * FROM v_sentiment_summary_dashboard;" 2>/dev/null | head -n 6

# Print completion message
echo -e "\n${GREEN}All steps completed successfully!${NC}"
echo -e "\n${YELLOW}=== Dashboard Views Available ===${NC}"
echo "- v_top10_trending_videos: Top 10 trending videos by engagement"
echo "- v_top10_videos_sentiment_analysis: Detailed sentiment analysis per video"
echo "- v_sentiment_summary_dashboard: Overall sentiment summary"
echo "- v_video_sentiment_details: Video ranking with sentiment breakdown"
echo "- v_sentiment_by_time: Sentiment trends over time"
echo -e "\n${GREEN}Sentiment analysis dashboard is ready!${NC}"