import pandas as pd
import os
from utils.file_name import FileNameGenerator
from utils.tiktok_data_clearning import DataCleaning
from datetime import datetime
import pytz

class TrendVideosProcessor:
    @staticmethod
    def extract_hashtags(text):
        import re
        return re.findall(r'#\w+', str(text))

    @staticmethod
    def remove_hashtags(text):
        import re
        return re.sub(r'#[\w]+', '', str(text)).strip()
    @staticmethod
    def extract_tiktok_username(url):
        import re
        match = re.search(r'tiktok\.com/@([\w\.]+)/video/', str(url))
        if match:
            return match.group(1)
        return None
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            # Only drop rows where all values are NaN
            cleaned_data = data.dropna(how='all')
            cleaned_data = cleaned_data.drop_duplicates()
            return cleaned_data
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return data

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            # Normalize likes, comments, shares if present
            for col in ['likes', 'comments', 'shares']:
                if col in data.columns:
                    data[col] = data[col].apply(lambda x: DataCleaning.convert_text_to_number(x))
            # Normalize time_published if present
            if 'time_published' in data.columns:
                hcm_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                def parse_timestamp(val):
                    ts = DataCleaning.convert_text_date_to_time_stamp(val)
                    if ts is None:
                        return None
                    try:
                        return datetime.fromtimestamp(ts, hcm_tz).strftime('%d-%m-%Y')
                    except Exception:
                        return None
                data['time_published'] = data['time_published'].apply(parse_timestamp)
            # Extract username from video_url if present
            if 'url' in data.columns:
                data['username'] = data['url'].apply(self.extract_tiktok_username)
            # Extract hashtags from title and remove them from title
            if 'title' in data.columns:
                data['hashtags'] = data['title'].apply(self.extract_hashtags)
                data['title'] = data['title'].apply(self.remove_hashtags)
            return data
        except Exception as e:
            print(f"Error normalizing data: {e}")
            return data

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        print("Starting trend videos data processing...")
        data = self.clean_data(data)
        data = self.normalize(data)
        # Drop duplicate rows based on 'video_url' if present
        if 'url' in data.columns:
            data = data.drop_duplicates(subset=['url'])
        print("Trend videos data processing completed.")
        return data
