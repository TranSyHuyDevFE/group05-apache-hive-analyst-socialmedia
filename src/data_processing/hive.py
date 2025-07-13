from pyhive import hive

# Establish connection to Hive
conn = hive.Connection(
    host='localhost',       # e.g., 'localhost' or a cluster node
    port=10000,                  # default HiveServer2 port
    auth='NONE'                  # adjust authentication if needed (e.g., 'KERBEROS')
)

# Create a cursor object
cursor = conn.cursor()

# Define the HiveQL query to create a new database
create_db_query = """
CREATE DATABASE IF NOT EXISTS company_db
"""

# Execute the query to create the database
cursor.execute(create_db_query)
print("Database 'company_db' created successfully.")

# Switch to the new database
use_db_query = "USE company_db"
cursor.execute(use_db_query)

# Define the HiveQL query to create a simple table in the new database
create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
    id INT,
    name STRING,
    department STRING,
    salary FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
"""

# Execute the query to create the table
cursor.execute(create_table_query)
print("Table 'employees' created successfully in 'company_db'.")

# Insert a simple value into the table
insert_query = """
INSERT INTO TABLE employees VALUES (1, 'Alice', 'HR', 50000.0)
"""
cursor.execute(insert_query)
print("Inserted one row into 'employees'.")

# Close the cursor and connection
cursor.close()
conn.close()
