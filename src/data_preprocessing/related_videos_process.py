import pandas as pd
import re
from .utils.tiktok_data_clearning import DataCleaning


class RelatedVideosProcessor:
    @staticmethod
    def extract_hashtags(text):
        return re.findall(r'#\w+', str(text))

    @staticmethod
    def extract_username(video_link):
        match = re.search(r'/@([\w\.]+)/video/', str(video_link))
        if match:
            return match.group(1)
        return None

    @staticmethod
    def extract_video_id(video_link):
        match = re.search(r'/video/(\d+)', str(video_link))
        if match:
            return match.group(1)
        return None

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            cleaned_data = data.dropna(how='all')
            cleaned_data = cleaned_data.drop_duplicates()
            return cleaned_data
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return data

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            # Normalize likes
            if 'likes' in data.columns:
                data['likes'] = data['likes'].apply(
                    lambda x: DataCleaning.convert_text_to_number(x))
            # Extract username and video_id from video_link
            if 'video_link' in data.columns:
                data['username'] = data['video_link'].apply(
                    self.extract_username)
                data['video_id'] = data['video_link'].apply(
                    self.extract_video_id)
            # Extract hashtags from title
            if 'title' in data.columns:
                data['hashtags'] = data['title'].apply(self.extract_hashtags)
            return data
        except Exception as e:
            print(f"Error normalizing data: {e}")
            return data

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        print("Starting related videos data processing...")
        data = self.clean_data(data)
        data = self.normalize(data)
        # Drop duplicate rows based on 'video_link' if present
        if 'video_link' in data.columns:
            data = data.drop_duplicates(subset=['video_link'])
        print("Related videos data processing completed.")
        return data
