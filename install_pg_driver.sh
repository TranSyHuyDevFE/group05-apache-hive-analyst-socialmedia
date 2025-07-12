#!/bin/bash

echo "Setting up Apache Hive cluster with PostgreSQL driver..."

# Create necessary directories
echo "Creating directories..."
mkdir -p lib
mkdir -p data/hive_db
mkdir -p data/warehouse

# Download PostgreSQL JDBC driver
echo "Downloading PostgreSQL JDBC driver..."
wget -O lib/postgresql.jar https://jdbc.postgresql.org/download/postgresql-42.7.2.jar

# Check if download was successful
if [ $? -eq 0 ]; then
    echo "PostgreSQL JDBC driver downloaded successfully!"
else
    echo "Failed to download PostgreSQL JDBC driver!"
    exit 1
fi

# Set proper permissions
echo "Setting permissions..."
chmod 755 data/hive_db
chmod 755 data/warehouse
chmod 644 lib/postgresql.jar

echo "Setup completed successfully!"
echo "You can now run: docker-compose up -d"
echo ""
echo "Services will be available at:"
echo "- Hive Metastore: localhost:9083"
echo "- HiveServer2: localhost:10000"
echo "- Superset: http://localhost:8088 (admin/admin)"
echo "- PostgreSQL: localhost:5432"
