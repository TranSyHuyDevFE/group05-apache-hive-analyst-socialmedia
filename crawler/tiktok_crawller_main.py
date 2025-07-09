# This file to handle TikTok crawling process"
from tiktok_video_related import TikTokVideoRelatedScraper
from tiktok_video_details import TikTokVideoDetailScraper
from tiktok_trend_videos  import TikTokVideoScraper
from datetime import datetime
import os
import pytz

class TikTokCrawlerMain:
    def __init__(self): 
        folder = self.build_folder()
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

    def _process_video_info(self, video_info):
        '''
          Process video info and add to queue
        '''
        print(f"Processing video info: {video_info}")
        video_url = video_info.get('video_url')
        # self.scraper.scrape_related_videos(video_url=video_url,)
        
    def run(self):
        '''
          Load full video
          Loop all video to get details
          Loop all video to get related videos
          Loop all video to get comments
        '''
        self.trend_scraper.scrape_videos_multi_tab_fast(
          max_categories=10,
        )
        # trigger to push to other process.

if __name__ == "__main__":
    crawler = TikTokCrawlerMain()
    crawler.build_folder()
    crawler.run()