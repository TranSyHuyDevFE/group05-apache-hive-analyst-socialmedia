#!/bin/bash
set -e

# Step 1: Create folders in warehouse for each table
target_dir="volumes/warehouse/tiktok"
declare -A tbls=(
  [category]=category.csv
  [comments]=comments.csv
  [related_videos]=related_videos.csv
  [video]=video_info.csv
  [video_info_details]=video_info_details.csv
)
for tbl in "${!tbls[@]}"; do
  mkdir -p "$target_dir/$tbl"
done

# Step 2: Copy each data file to its folder
src_dir="crawler/raw_data/tiktok"
for tbl in "${!tbls[@]}"; do
  cp "$src_dir/${tbls[$tbl]}" "$target_dir/$tbl/"
done

# Step 3: Copy scripts folder to warehouse
rm -rf "$target_dir/scripts"
cp -r scripts "$target_dir/"

# Step 4: Execute create_tables.hql using docker beeline
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/create-tables.hql
# Step 5: Execute create-views.hql using docker beeline
docker exec -i hiveserver2 beeline -u jdbc:hive2://localhost:10000 -f /opt/hive/data/warehouse/scripts/create-views.hql

echo "All steps completed successfully."