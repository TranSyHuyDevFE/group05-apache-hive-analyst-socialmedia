#!/bin/bash
set -e

# Step 1: Create folders in warehouse for each table
target_dir_data="volumes/warehouse/tiktok"
target_dir_script="volumes/warehouse"
declare -A tbls=(
  [category]=category.csv
  [comments]=comments.csv
  [related_videos]=related_videos.csv
  [video]=video_info.csv
  [video_info_details]=video_info_details.csv
  [user_info_details]=user_info_details.csv
)
for tbl in "${!tbls[@]}"; do
  mkdir -p "$target_dir_data/$tbl"
done

# Step 2: Copy each data file to its folder
src_dir="cleaned_data"
for tbl in "${!tbls[@]}"; do
  cp -r "$src_dir/$tbl/." "$target_dir_data/$tbl/"
done

# Step 3: Copy scripts folder to warehouse
rm -rf "$target_dir_script/scripts"
cp -r scripts "$target_dir_script/"

# Step 4: Remove database structure
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/remove-db-structure.hql

# Step 5: Execute create_tables.hql using docker beeline
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/create-tables.hql
# Step 6: Execute create-views.hql using docker beeline
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/create-views.hql

echo "All steps completed successfully."