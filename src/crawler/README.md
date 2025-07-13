# Trình Thu Thập Nội Dung Truyền Thông Xã Hội

## Tính Năng
1. **Thu Thập Danh Mục**  
  Trích xuất danh mục từ các nền tảng truyền thông xã hội.

2. **Thu Thập Video Xu Hướng**  
  Xác định và lấy các video xu hướng.

3. **Xử Lý Video Xu Hướng**  
  Lặp qua các video xu hướng để thu thập thông tin chi tiết:
  - Bình luận
  - Thông tin Video
  - Video Liên Quan

4. **Xử Lý Video Liên Quan**  
  Xử lý các video liên quan để có thêm thông tin chi tiết.

## Ghi Chú
- Đảm bảo xử lý đúng giới hạn tốc độ API.
- Xác thực và làm sạch dữ liệu trước khi lưu trữ.
- Tối ưu hóa vòng lặp để cải thiện
- Implement error handling for network issues.
- Consider privacy and ethical guidelines when crawling data.

# TODO:
- [ ] Group excel data by date
- [ ] Create job to run every day.


# Start: 
```
supervisord -c supervisord.conf 
```