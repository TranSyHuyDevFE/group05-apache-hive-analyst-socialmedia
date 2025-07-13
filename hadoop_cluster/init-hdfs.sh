#!/bin/bash
set -e

# Start the namenode in the background
hdfs namenode &
NAMENODE_PID=$!

# Wait for HDFS to be ready
for i in {1..30}; do
  if hdfs dfs -ls / >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

# Create HDFS user directory for dr.who and set permissions
hdfs dfs -mkdir -p /user/dr.who
hdfs dfs -chown dr.who:supergroup /user/dr.who
hdfs dfs -chmod 777 /user/dr.who

# Create HDFS warehouse directory for hive and set permissions
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chmod 777 /user/hive/warehouse

# Set ownership and write permissions on root directory
hdfs dfs -chown dr.who:supergroup /
hdfs dfs -chmod 777 /

# Wait for the namenode process to finish
wait $NAMENODE_PID
