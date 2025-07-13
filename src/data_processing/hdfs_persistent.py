from hdfs import InsecureClient

# HDFS connection details
hdfs_url = 'http://localhost:9870'  # Correct WebHDFS port exposed by namenode in your docker-compose
hdfs_user = 'root'  # or your HDFS user

# Local CSV file path
local_csv_path = 'employees.csv'

# Target HDFS path
hdfs_target_path = '/user/hive/warehouse/employees/employees.csv'

# Connect to HDFS
client = InsecureClient(hdfs_url, user=hdfs_user)

# Upload the CSV file to HDFS
client.upload(hdfs_target_path, local_csv_path, overwrite=True)
print(f"Uploaded {local_csv_path} to HDFS at {hdfs_target_path}")