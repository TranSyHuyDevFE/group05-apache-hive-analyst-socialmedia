# This file to handle TikTok crawling process"
from tiktok_video_related import TikTokVideoRelatedScraper
from tiktok_video_details import TikTokVideoDetailScraper
from tiktok_trend_videos  import TikTokVideoScraper
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
      '''
      create folder with name dd_mm_yyyy_hh_mm_ss/
      '''
      from datetime import datetime
      import os
      folder_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
      os.makedirs(os.path.join(base_dir, folder_name), exist_ok=True)
      print(f"Created folder: {folder_name}")
      return os.path.join(base_dir, folder_name)

    def _cancel_wrapper(self, func, timeout=100):
      '''
      '''
      import threading
      def wrapper():
        try:
          func()
        except Exception as e:
          print(f"Function execution interrupted: {e}")
      thread = threading.Thread(target=wrapper)
      thread.start()
      thread.join(timeout=timeout)  # Wait for specified timeout
      if thread.is_alive():
        print(f"Function execution exceeded {timeout} seconds and was canceled.")
        # Optionally, you can terminate the thread here, but Python threads cannot be forcefully killed.
    def run(self):
        '''
          Load full video
          Loop all video to get details
          Loop all video to get related videos
          Loop all video to get comments
        '''

        self._cancel_wrapper(self.trend_scraper.scrape_videos())
        # trigger to push to other process.
        
        
if __name__ == "__main__":
    crawler = TikTokCrawlerMain()
    crawler.build_folder()
    crawler.run()