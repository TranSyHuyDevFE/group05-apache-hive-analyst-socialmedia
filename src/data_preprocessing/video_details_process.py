import pandas as pd
import json
from .utils.tiktok_data_clearning import DataCleaning
from datetime import datetime
import pytz  # Add this import for timezone handling


import ast


class VideoDetailsProcessor:
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            cleaned_data = data.dropna()
            cleaned_data = cleaned_data.drop_duplicates()
            return cleaned_data
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return data  # Return original data to avoid breaking the pipeline

    @staticmethod
    def parse_json_flexible(val):
        if pd.isnull(val):
            return None
        # Try JSON loads directly
        try:
            return json.loads(val)
        except Exception:
            pass
        # Try literal_eval (for single-quoted dicts)
        try:
            return ast.literal_eval(val)
        except Exception:
            pass
        # Try fixing double-escaped JSON
        try:
            fixed = val.replace('""', '"').replace("'", '"')
            return json.loads(fixed)
        except Exception:
            pass
        return None

    def split_json_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            # Parse JSON-like columns robustly
            for column in ['author', 'music', 'engagement']:
                if column in data.columns:
                    data[column +
                         '_dict'] = data[column].apply(self.parse_json_flexible)

            # Extract fields from parsed dicts
            if 'author_dict' in data.columns:
                data['username'] = data['author_dict'].apply(
                    lambda x: x.get('username') if isinstance(x, dict) else None)
                data['nickname'] = data['author_dict'].apply(
                    lambda x: x.get('nickname') if isinstance(x, dict) else None)
            if 'music_dict' in data.columns:
                data['music_title'] = data['music_dict'].apply(
                    lambda x: x.get('title') if isinstance(x, dict) else None)
                data['music_link'] = data['music_dict'].apply(
                    lambda x: x.get('link') if isinstance(x, dict) else None)
            if 'engagement_dict' in data.columns:
                data['likes'] = data['engagement_dict'].apply(
                    lambda x: x.get('likes') if isinstance(x, dict) else None)
                data['comments'] = data['engagement_dict'].apply(
                    lambda x: x.get('comments') if isinstance(x, dict) else None)
                data['shares'] = data['engagement_dict'].apply(
                    lambda x: x.get('shares') if isinstance(x, dict) else None)

            # Drop original and intermediate columns
            drop_cols = [col for col in ['author', 'music', 'engagement',
                                         'author_dict', 'music_dict', 'engagement_dict'] if col in data.columns]
            data = data.drop(columns=drop_cols)
            return data
        except Exception as e:
            print(f"Error splitting JSON columns: {e}")
            return data

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            # Define Asia/Ho_Chi_Minh timezone
            hcm_tz = pytz.timezone('Asia/Ho_Chi_Minh')

            # Normalize date field using convert_text_date_to_time_stamp
            if 'time_published' in data.columns:
                data['time_published'] = data['time_published'].apply(
                    lambda x: DataCleaning.convert_text_date_to_time_stamp(x)
                )
                # Convert timestamp to 'dd-mm-yyyy' format in HCM timezone
                data['time_published'] = data['time_published'].apply(
                    lambda x: datetime.fromtimestamp(
                        x, hcm_tz).strftime('%d-%m-%Y') if x else None
                )

            # Normalize numeric fields using convert_text_to_number
            for field in ['likes', 'comments', 'shares']:
                if field in data.columns:
                    data[field] = data[field].apply(
                        lambda x: DataCleaning.convert_text_to_number(x)
                    )
                    print(f"After normalizing '{field}':", data[field].head())

            if 'hashtags' in data.columns:
                data['hashtags'] = data['hashtags'].apply(
                    lambda x: [tag for tag in eval(x) if tag.startswith(
                        '#')] if pd.notnull(x) else None
                )
            return data
        except Exception as e:
            print(f"Error normalizing data: {e}")
            return data

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        print("Starting processing...")
        data = self.clean_data(data)
        data = self.split_json_columns(data)
        data = self.normalize(data)
        # Drop duplicate rows based on 'video_url' column if it exists
        if 'video_url' in data.columns:
            before = len(data)
            data = data.drop_duplicates(subset=['video_url'])
            after = len(data)
        print("Processing completed.")
        return data
