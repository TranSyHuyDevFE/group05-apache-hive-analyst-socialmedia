
import pandas as pd
import os
from utils.file_name import FileNameGenerator
from utils.tiktok_data_clearning import DataCleaning
from datetime import datetime
import pytz

class CommentDetailsProcessor:
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            cleaned_data = data.dropna(subset=["username", "content", "video_url"])
            cleaned_data = cleaned_data.drop_duplicates()
            return cleaned_data
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return data

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            # Clean username: extract before '?' if present
            if 'username' in data.columns:
                data['username'] = data['username'].apply(lambda x: str(x).split('?')[0] if pd.notnull(x) else x)
            # Normalize 'likes' using DataCleaning.convert_text_to_number
            if 'likes' in data.columns:
                data['likes'] = data['likes'].apply(lambda x: DataCleaning.convert_text_to_number(x))
            # Normalize 'timestamp' using DataCleaning.convert_text_date_to_time_stamp, then format to 'dd-mm-yyyy' in HCM timezone
            if 'timestamp' in data.columns:
                hcm_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                def parse_timestamp(val):
                    ts = DataCleaning.convert_text_date_to_time_stamp(val)
                    if ts is None:
                        return None
                    try:
                        return datetime.fromtimestamp(ts, hcm_tz).strftime('%d-%m-%Y')
                    except Exception:
                        return None
                data['timestamp'] = data['timestamp'].apply(parse_timestamp)
            return data
        except Exception as e:
            print(f"Error normalizing data: {e}")
            return data

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        print("Starting comment data processing...")
        data = self.clean_data(data)
        data = self.normalize(data)
        # Drop duplicate rows based on 'username', 'content', 'video_url'
        if all(col in data.columns for col in ['username', 'content', 'video_url']):
            data = data.drop_duplicates(subset=['username', 'content', 'video_url'])
        print("Comment data processing completed.")
        return data
