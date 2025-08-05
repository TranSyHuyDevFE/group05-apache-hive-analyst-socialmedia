FROM python:3.10-slim

WORKDIR /app

# Copy toàn bộ file cần thiết
COPY main.py /app/main.py
COPY crontab.txt /app/crontab.txt

# Cài đặt cron và tạo symlink cho python3
RUN apt-get update && apt-get install -y cron && \
    ln -s /usr/local/bin/python /usr/bin/python3

# Cài đặt cronjob
RUN crontab /app/crontab.txt

# Tạo file log rỗng để tránh lỗi
RUN touch /var/log/cron.log

# Giữ container luôn chạy và in log ra terminal
CMD cron && tail -f /var/log/cron.log
