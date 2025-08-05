import pandas as pd
from transformers import pipeline
import re
import string
from underthesea import word_tokenize
import os


class TextProcessing:
    def __init__(self):
        self.stopwords = TextProcessing.read_stopwords(
            "vietnamese_stopwords.txt")

    def clean_text(self, text):
        text = str(text) if text is not None else ""
        if text is None:
            return ""
        text = text.lower()
        text = text.translate(str.maketrans(
            '', '', string.punctuation + '“”‘’…'))
        text = re.sub(r'\d+', '', text)
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    def tokenize(self, text):
        cleaned = self.clean_text(text)
        return word_tokenize(cleaned, format="text").split()

    def remove_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stopwords]

    @staticmethod
    def read_stopwords(filepath):
        """Read Vietnamese stopwords from a file in the same directory as this script, one per line."""
        dir_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(dir_path, filepath)
        with open(full_path, encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]


class SentimentAnalyzer:
    def __init__(self, model_path='5CD-AI/Vietnamese-Sentiment-visobert', max_tokens=68):
        self.sentiment_task = pipeline(
            "sentiment-analysis", model=model_path, tokenizer=model_path)
        self.tp = TextProcessing()
        self.max_tokens = max_tokens

    def get_sentiment(self, text):
        # Xu ly text
        cleaned = self.tp.clean_text(text)
        tokens = self.tp.tokenize(cleaned)
        tokens = tokens[:self.max_tokens]
        filtered_text = ' '.join(self.tp.remove_stopwords(tokens))

        # Xu ly phan loai cam xuc
        result = self.sentiment_task(filtered_text)[0]

        return result['label']

    def analyze(self, df, text_column):
        df = df.copy()
        df['sentiment'] = df[text_column].apply(self.get_sentiment)
        return df


# if __name__ == "__main__":
#     sample_text = "Xin chào! Đây là một ví dụ về xử lý văn bản số 123, với dấu câu và ký tự đặc biệt…"
#     tp = TextProcessing()
#     print("Original:", sample_text)
#     cleaned = tp.clean_text(sample_text)
#     tokens = tp.tokenize(cleaned)
#     filtered = tp.remove_stopwords(tokens)
#     print("Filtered (no stopwords):", filtered)

#     # Example usage with a pandas DataFrame
#     data = {
#         "text": [
#             "Tôi rất thích sản phẩm này!",
#             "Dịch vụ quá tệ, tôi không hài lòng.",
#             "Bình thường, không có gì đặc biệt.",
#             "Sản phẩm tuyệt vời, giao hàng nhanh.",
#             "Tôi sẽ không mua lại lần sau."
#         ]
#     }
#     df = pd.DataFrame(data)
#     analyzer = SentimentAnalyzer()
#     result_df = analyzer.analyze(df, "text")
#     print(result_df[["text", "sentiment"]])
