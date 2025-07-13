# This file to handle TikTok crawling process"
from tiktok_video_related import TikTokVideoRelatedScraper
from tiktok_video_details import TikTokVideoDetailScraper
from tiktok_trend_videos  import TikTokVideoScraper
from datetime import datetime
import os
import pytz
import json
import pandas as pd

class TikTokCrawlerMain:
    def __init__(self): 
        folder = self.build_folder()
        self.conf_json_path = os.path.join(folder, "crawl_config.json")
        self.scraper = TikTokVideoRelatedScraper(
            base_dir=folder,
            output_file="related_videos.csv"
        )
        self.detail_scraper = TikTokVideoDetailScraper(
            base_dir=folder,
            output_file="details_video_info.csv"
        )
        self.trend_scraper = TikTokVideoScraper(
            base_dir=folder,
            output_file="trend_videos.csv"
        )
          
    def build_folder(self, base_dir='raw_data/tiktok'):
      hcm_tz = pytz.timezone('Asia/Ho_Chi_Minh')
      folder_name = datetime.now(hcm_tz).strftime("date_%d_%m_%Y_time_%H_%M")
      os.makedirs(os.path.join(base_dir, folder_name), exist_ok=True)
      print(f"Created folder: {folder_name}")
      return os.path.join(base_dir, folder_name)

    def load_crawl_config(self):
        """Load crawl configuration from JSON file"""
        if not os.path.exists(self.conf_json_path):
            return {
                "last_video_id": "",
                "status": "initialized",
                "timestamp": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat()
            }
        
        try:
            with open(self.conf_json_path, 'r', encoding='utf-8') as file:
                config = json.load(file)
                return config
        except Exception as e:
            print(f"Error loading config: {e}")
        
        return {
            "last_video_id": "",
            "status": "error",
            "timestamp": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat()
        }

    def save_crawl_config(self, last_video_id="", status="running"):
        """Save crawl configuration to JSON file"""
        hcm_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        config_data = {
            "last_video_id": last_video_id,
            "status": status,
            "timestamp": datetime.now(hcm_tz).isoformat()
        }
        
        try:
            with open(self.conf_json_path, 'w', encoding='utf-8') as file:
                json.dump(config_data, file, indent=2, ensure_ascii=False)
            print(f"Saved config: {config_data}")
        except Exception as e:
            print(f"Error saving config: {e}")

    def load_downloaded_videos(self):
        """Load downloaded video data from CSV file"""
        trend_csv_path = os.path.join(os.path.dirname(self.conf_json_path), "trend_videos.csv")
        
        if not os.path.exists(trend_csv_path):
            print(f"No trend videos file found at: {trend_csv_path}")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(trend_csv_path)
            print(f"Loaded {len(df)} videos from trend_videos.csv")
            return df
        except Exception as e:
            print(f"Error loading video data: {e}")
            return pd.DataFrame()

    def extract_video_ids_from_urls(self, df):
        """Extract video IDs from TikTok URLs"""
        if df.empty or 'url' not in df.columns:
            return []
        
        video_ids = []
        for url in df['url']:
            try:
                # Extract video ID from URL like: https://www.tiktok.com/@username/video/7523193842590338312
                video_id = url.split('/video/')[-1].split('?')[0]
                video_ids.append(video_id)
            except Exception as e:
                print(f"Error extracting video ID from {url}: {e}")
                video_ids.append("")
        
        return video_ids

    def run(self):
        '''
          Load full video
          Loop all video to get details
          Loop all video to get related videos
          Loop all video to get comments
        '''
        # Load previous configuration
        config = self.load_crawl_config()
        print(f"Loaded config: {config}")
        
        # Update status to running
        self.save_crawl_config(config.get("last_video_id", ""), "running")
        
        try:
            # Step 1: Scrape trending videos
            self.trend_scraper.scrape_videos_multi_tab_fast(
              max_categories=1,
              max_rounds=2.
            )
            
            # Step 2: Load downloaded video data
            video_df = self.load_downloaded_videos()
            if not video_df.empty:
                video_urls = video_df['url'].tolist()
                print(f"Loaded {len(video_urls)} video URLs for processing")
                
                # Update config with last video URL
                if video_urls:
                    last_video_url = video_urls[-1]
                    self.save_crawl_config(last_video_url, "processing_details")
            
            # Step 3: Loop all videos to get details
            for idx, row in video_df.iterrows():
                video_url = row['url']
                print(f"Processing details for: {video_url}")
                self.detail_scraper.scrape_detail_page(video_url)

            # Step 4: Loop all videos to get related videos
            if not video_df.empty:
                self.save_crawl_config(config.get("last_video_id", ""), "processing_related")
                # Process related videos for each video
                for idx, row in video_df.iterrows():
                    try:
                        video_url = row['url']
                        print(f"Processing related videos for: {video_url}")
                        # Add related video processing logic here
                        # self.scraper.scrape_related_videos(video_url)
                    except Exception as e:
                        print(f"Error processing related videos for row {idx}: {e}")
            
            # Update status to completed
            self.save_crawl_config(config.get("last_video_id", ""), "completed")
            
        except Exception as e:
            print(f"Error during crawling: {e}")
            self.save_crawl_config(config.get("last_video_id", ""), "error")
            raise

if __name__ == "__main__":
    crawler = TikTokCrawlerMain()
    crawler.run()