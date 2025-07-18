import pandas as pd
import json
from utils.tiktok_data_clearning import DataCleaning
from datetime import datetime
import pytz  # Add this import for timezone handling


class VideoDetailsProcessor:
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            cleaned_data = data.dropna()
            cleaned_data = cleaned_data.drop_duplicates()
            return cleaned_data
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return data  # Return original data to avoid breaking the pipeline

    def split_json_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            for column in ['author', 'music', 'engagement']:
                if column in data.columns:
                    data[column] = data[column].apply(
                        lambda x: x.replace("'", '"') if pd.notnull(x) else x
                    )

            # Extract JSON fields from specific columns
            data['username'] = data['author'].apply(
                lambda x: json.loads(x).get('username') if pd.notnull(x) else None)
            data['nickname'] = data['author'].apply(
                lambda x: json.loads(x).get('nickname') if pd.notnull(x) else None)

            # Additional fields from 'music' column
            data['music_title'] = data['music'].apply(
                lambda x: json.loads(x).get('title') if pd.notnull(x) else None)
            data['music_link'] = data['music'].apply(
                lambda x: json.loads(x).get('link') if pd.notnull(x) else None)

            # Additional fields from 'engagement' column
            data['likes'] = data['engagement'].apply(
                lambda x: json.loads(x).get('likes') if pd.notnull(x) else None)
            data['comments'] = data['engagement'].apply(
                lambda x: json.loads(x).get('comments') if pd.notnull(x) else None)
            data['shares'] = data['engagement'].apply(
                lambda x: json.loads(x).get('shares') if pd.notnull(x) else None)

            # Drop original JSON columns
            data = data.drop(columns=['author', 'music', 'engagement'])
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
                print("After normalizing 'time_published':",
                      data['time_published'].head())

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
        print("Processing completed.")
        return data
