# Installations
pip install -r requirements.txt
python3 sentiment.py

# Mmodel:
https://huggingface.co/5CD-AI/Vietnamese-Sentiment-visobert
Max lenght 256

# Xử lý nhận diện đâu là văn bản mang tính tích cực đâu là văn bản mang tính tiêu cực
Về điểm sentiment (cảm xúc):
NEU (Trung lập)
NEG (Tiêu cực)	
POS (Tích cực)	

# Flow chay
1. Crawll comment
2. Preprocessing data
3. run main.py to analysis

# TODO
[ ] Văn bản dài quá thì không đưa vào model xử lý dược rồi làm sao?
[ ] Ghép vô chổ chạy tự động khi job clean data chạy xong.