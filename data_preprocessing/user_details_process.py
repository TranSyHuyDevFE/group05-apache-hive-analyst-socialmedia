
import pandas as pd
import json
import ast
from typing import Any

class UserDetailsProcessor:
    @staticmethod
    def parse_json_flexible(val: Any):
        if pd.isnull(val):
            return None
        # Try JSON loads directly
        try:
            return json.loads(val)
        except Exception:
            pass
        # Try literal_eval (for single-quoted dicts or lists)
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
            # Parse 'counts' and 'links' columns
            if 'counts' in data.columns:
                data['counts_dict'] = data['counts'].apply(self.parse_json_flexible)
            if 'links' in data.columns:
                data['links_list'] = data['links'].apply(self.parse_json_flexible)

            # Extract fields from 'counts_dict'
            if 'counts_dict' in data.columns:
                data['following'] = data['counts_dict'].apply(lambda x: x.get('following') if isinstance(x, dict) else None)
                data['followers'] = data['counts_dict'].apply(lambda x: x.get('followers') if isinstance(x, dict) else None)
                data['likes'] = data['counts_dict'].apply(lambda x: x.get('likes') if isinstance(x, dict) else None)

            # Extract first link url/text if available
            if 'links_list' in data.columns:
                data['first_link_url'] = data['links_list'].apply(lambda x: x[0]['url'] if isinstance(x, list) and x and isinstance(x[0], dict) and 'url' in x[0] else None)
                data['first_link_text'] = data['links_list'].apply(lambda x: x[0]['text'] if isinstance(x, list) and x and isinstance(x[0], dict) and 'text' in x[0] else None)

            # Drop original and intermediate columns
            drop_cols = [col for col in ['counts', 'links', 'counts_dict', 'links_list'] if col in data.columns]
            data = data.drop(columns=drop_cols)
            return data
        except Exception as e:
            print(f"Error splitting JSON columns: {e}")
            return data

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        print("Starting user details processing...")
        # Drop NA and duplicates
        data = data.dropna()
        data = data.drop_duplicates()
        data = self.split_json_columns(data)
        # Drop duplicate rows by username if exists
        if 'username' in data.columns:
            data = data.drop_duplicates(subset=['username'])
        print("User details processing completed.")
        return data
