import glob
from pyhive import hive

# Kết nối HiveServer2 (sửa lại host, port, username nếu cần)
conn = hive.Connection(host='localhost', port=10000, username='hive')
cursor = conn.cursor()

# Apply tất cả các bảng trước
table_files = sorted(glob.glob('databases/tables/*.hsql'))
for file in table_files:
    print(f"Applying table: {file}")
    with open(file) as f:
        ddl = f.read()
    cursor.execute(ddl)

# Sau đó apply các view
view_files = sorted(glob.glob('databases/views/*.hsql'))
for file in view_files:
    print(f"Applying view: {file}")
    with open(file) as f:
        ddl = f.read()
    cursor.execute(ddl)

print("Migration completed.")
cursor.close()
conn.close()
