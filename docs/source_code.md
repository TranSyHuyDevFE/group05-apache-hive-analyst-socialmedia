# Mô tả source code:

### 📁 **background_job**
- **Mục đích**: Chứa các job chạy nền (background processes)
- **Công dụng**: Xử lý các tác vụ tự động như thu thập dữ liệu định kỳ, làm sạch dữ liệu, và các pipeline ETL

### 📁 **build.sh**
- **Mục đích**: Script build và triển khai ứng dụng
- **Công dụng**: Tự động hóa quá trình build Docker images, cài đặt dependencies và khởi tạo môi trường

### 📁 **cleaned_data**
- **Mục đích**: Lưu trữ dữ liệu đã được làm sạch
- **Công dụng**: Chứa dữ liệu sau khi đã qua bước tiền xử lý, loại bỏ noise và chuẩn hóa định dạng

### 📁 **conf**
- **Mục đích**: Cấu hình hệ thống
- **Công dụng**: Chứa các file config cho Hive, Hadoop, database connections và các tham số hệ thống

### 📁 **docker-compose.yml**
- **Mục đích**: Orchestration các services Docker
- **Công dụng**: Định nghĩa và quản lý multi-container Docker application (Hive, PostgreSQL, Superset, etc.)

### 📁 **docs**
- **Mục đích**: Tài liệu dự án
- **Công dụng**: Chứa documentation, hướng dẫn sử dụng, kiến trúc hệ thống và mô tả source code

### 📁 **Dockerfile**
- **Mục đích**: Build Docker image
- **Công dụng**: Định nghĩa các bước build container image cho ứng dụng

### 📁 **entrypoint.sh**
- **Mục đích**: Script khởi tạo container
- **Công dụng**: Entry point cho Docker container, thiết lập môi trường và khởi động services

### 📁 **install_pg_driver.sh**
- **Mục đích**: Cài đặt PostgreSQL driver
- **Công dụng**: Script tự động cài đặt JDBC driver để kết nối Hive với PostgreSQL

### 📁 **lib**
- **Mục đích**: Thư viện và dependencies
- **Công dụng**: Chứa các JAR files, external libraries và custom UDFs cần thiết cho Hive

### 📁 **scripts**
- **Mục đích**: Scripts tiện ích
- **Công dụng**: Các shell scripts, Python scripts để automation các tác vụ như backup, monitoring, deployment

### 📁 **sentiment**
- **Mục đích**: Phân tích cảm xúc (Sentiment Analysis)
- **Công dụng**: Chứa models, algorithms và scripts để phân tích sentiment của dữ liệu mạng xã hội

### 📁 **src** 
- **Mục đích**: Source code chính

### 📁 **superset**
- **Mục đích**: Apache Superset configuration
- **Công dụng**: Cấu hình và customization cho dashboard và visualization tool

### 📁 **transformed_data**
- **Mục đích**: Dữ liệu đã được chuyển đổi
- **Công dụng**: Lưu trữ dữ liệu sau khi đã qua các bước transformation và ready for analysis

### 📁 **volumes**
- **Mục đích**: Docker volumes
- **Công dụng**: Persistent storage cho các Docker containers, đảm bảo dữ liệu không bị mất khi restart containers

## Luồng xử lý dữ liệu
1. **Thu thập dữ liệu**: `background_job` → Raw data
2. **Làm sạch dữ liệu**: Raw data → `cleaned_data`
3. **Chuyển đổi dữ liệu**: `cleaned_data` → `transformed_data`
4. **Phân tích**: `hive` + `sentiment` → `report`
5. **Visualization**: `superset` dashboard

## Công nghệ sử dụng
- **Apache Hive**: Data warehouse và SQL-like queries
- **Docker**: Containerization
- **PostgreSQL**: Metadata store
- **Apache Superset**: Data visualization
- **Python/Shell**: Scripting và automation
