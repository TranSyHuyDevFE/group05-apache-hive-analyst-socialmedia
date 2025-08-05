# This file to handle TikTok crawling process"
from .tiktok_video_related import TikTokVideoRelatedScraper
from .tiktok_video_details import TikTokVideoDetailScraper
from .tiktok_user_info import TikTokUserInfoScraper
from .tiktok_trend_videos import TikTokVideoScraper
from datetime import datetime
import os
import pytz
import json
import pandas as pd
from enum import Enum
from .compressor import CrawledDataCompressor
# from sync_data_to_git import run_sync_script
import time

# from scheduler import HourlyScheduler


class TikTokCrawlerIO:
    @staticmethod
    def build_folder(base_dir='./data/raw_data/tiktok'):
        hcm_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        # folder_name = datetime.now(hcm_tz).strftime("date_%d_%m_%Y_time_%H")
        # os.makedirs(os.path.join(base_dir, folder_name), exist_ok=True)
        os.makedirs(os.path.join(base_dir), exist_ok=True)
        return os.path.join(base_dir)

    @staticmethod
    def get_default_config_path():
        return os.path.join(os.path.dirname(__file__), "crawl_config.json")

    @staticmethod
    def duplicate_config(conf_json_path, folder):
        '''
        Create a clone of crawl_config.json to the specified folder if it does not already exist,
        and add a current timestamp to each item in the configuration.
        '''
        output_path = os.path.join(folder, "crawl_config.json")
        if os.path.exists(output_path):
            print(f"Configuration file already exists at: {output_path}")
            return output_path

        if os.path.exists(conf_json_path):
            with open(conf_json_path, 'r') as f:
                config_data = json.load(f)

            # Add current timestamp to each item
            current_time = datetime.now(
                pytz.timezone('Asia/Ho_Chi_Minh')).isoformat()
            for item in config_data:
                item['timestamp'] = current_time

            with open(output_path, 'w') as f:
                json.dump(config_data, f, indent=4)
            print(f"Configuration file duplicated to: {output_path}")
            return output_path
        else:
            print(f"Configuration file not found at: {conf_json_path}")
            return None

    @staticmethod
    def load_config_from_directory(config_path):
        '''
        Load configuration from a JSON file and cast it to CrawllerConf
        '''
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            print(f"Configuration loaded from: {config_path}")
            return CrawllerConf(config_path, config_data)
        else:
            print(f"Configuration file not found at: {config_path}")
            return CrawllerConf([])


class ProcessStatus(Enum):
    NOT_STARTED = 'not_started'
    CRAWLING_LIST_VIDEO = 'crawling_list_video'
    CRAWLED_LIST_VIDEO = 'crawled_list_video'
    CRAWLING_DETAILS_VIDEO = 'crawling_details_video'
    CRAWLED_DETAILS_VIDEO = 'crawled_details_video'
    CRAWLING_USER_INFO = 'crawling_user_info'
    CRAWLED_USER_INFO = 'crawled_user_info'
    CRAWLING_RELATED_VIDEO = 'crawling_related_video'
    FINISH = 'finish'


class CrawllerConf:
    def __init__(self, path, config_list):
        self.path = path
        self.config_list = config_list

    def _get_current_time(self):
        return datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat()

    def get_by_slug(self, slug):
        for c in self.config_list:
            if c['category_slug'] == slug:
                return c
        return None

    def ensure_categories(self, categories):
        for slug in categories:
            if not any(c['category_slug'] == slug for c in self.config_list):
                self.config_list.append({
                    'category_slug': slug,
                    'total_video_crawlled': 0,
                    'timestamp': self._get_current_time(),
                    'status': 'not_started'
                })

    def update_status(self, slug: str, status: ProcessStatus):
        conf = self.get_by_slug(slug)
        if conf:
            conf['status'] = status.value
            conf['timestamp'] = self._get_current_time()
            self.persist()

    def update_total_video(self, slug, total):
        conf = self.get_by_slug(slug)
        if conf:
            conf['total_video_crawlled'] = total
            conf['timestamp'] = self._get_current_time()
            self.persist()

    def to_list(self):
        return self.config_list

    def persist(self,):
        with open(self.path, 'w') as f:
            json.dump(self.config_list, f, indent=4)

    def get_category_by_status(self, status: ProcessStatus):
        """
        Get all categories with the specified status
        """
        return [c for c in self.config_list if c['status'] == status.value]


'''
Target
- Load configuration from JSON file
- [{ category_slug, total_video_crawlled, timestamp, status: 'not_started' |'crawling_list_video' | 'crawlling_details_video' | 'crawling_related_video' | 'finish'}]
- Process: crawl list video by category then update status to crawling_list_video 
- Process: crawl details video by category then update status to crawling_details_video 
- Process: crawl related video by category then update status to crawling_related_video
- after all step update status to finish
- build docker image then setup to server schedule every hour cralled videos then update to drive.
'''


class TikTokCrawlerMain:
    def __init__(self):
        self.io = TikTokCrawlerIO
        self.folder = self.io.build_folder()
        self.scraper = TikTokVideoRelatedScraper(
            base_dir=self.folder,
            output_file="related_videos.csv"
        )
        self.detail_scraper = TikTokVideoDetailScraper(
            base_dir=self.folder,
            output_file="details_video_info.csv"
        )
        self.trend_scraper = TikTokVideoScraper(
            base_dir=self.folder,
            output_file="trend_videos.csv"
        )

        self.user_info_scraper = TikTokUserInfoScraper(
            base_dir=self.folder,
            output_file="user_info.csv"
        )
        self.compressor = CrawledDataCompressor()

    def load_trend_videos_crawled_by_category(self, category_slug):
        """
        Load trend videos that have been crawled by category slug and filter by the given category_slug.
        Returns the result as an array of JSON objects.
        """
        trend_videos_path = os.path.join(self.folder, "trend_videos.csv")
        if os.path.exists(trend_videos_path):
            df = pd.read_csv(trend_videos_path)
            filtered_df = df[df['category'] == category_slug]
            # Convert DataFrame to array of JSON objects
            return filtered_df.to_dict(orient='records')
        else:
            print(f"Trend videos file not found at: {trend_videos_path}")
            return []

    def run(self):
        MAX_VIDESO_URL_PER_CATEGORY = 259
        # Always load config from default path
        target_conf_path = self.io.duplicate_config(
            self.io.get_default_config_path(),  self.io.build_folder())
        crawl_config = self.io.load_config_from_directory(target_conf_path)

        # Start the crawling process for each category
        category_not_started = crawl_config.get_category_by_status(
            ProcessStatus.NOT_STARTED)
        if category_not_started:
            for category in category_not_started:
                crawl_config.update_status(
                    category['category_slug'], ProcessStatus.CRAWLING_LIST_VIDEO)
                self.trend_scraper.scrape_videos_by_one_category(
                    category, max_crawled_items=MAX_VIDESO_URL_PER_CATEGORY)
                crawl_config.update_status(
                    category['category_slug'], ProcessStatus.CRAWLED_LIST_VIDEO)

        print(
            f"Finished crawling. Total categories processed: {len(crawl_config.to_list())}"
        )

        # Optimize performnace it take about 10 - 15 seoncd for one vid -> 700vid -> 7000s = 2 hours
        category_crawled_video_list = crawl_config.get_category_by_status(
            ProcessStatus.CRAWLED_LIST_VIDEO)
        # if category_crawled_video_list:
        #     for category in category_crawled_video_list:
        #         crawl_config.update_status(
        #             category['category_slug'], ProcessStatus.CRAWLING_USER_INFO)
        #         video_urls = [video['url'] for video in self.load_trend_videos_crawled_by_category(
        #             category['category_slug'])]

        #         user_url_crawler_chunks = [video_urls[i:i + 20]
        #                                    for i in range(0, len(video_urls), 20)]
        #         for chunk in user_url_crawler_chunks:
        #             usernames = [url.split('/')[3].replace('@', '')
        #                          for url in chunk]
        #             self.user_info_scraper.scrape_multiple_users(usernames)
        #         crawl_config.update_status(
        #             category['category_slug'], ProcessStatus.CRAWLED_USER_INFO)

        # category_crawled_video_list = crawl_config.get_category_by_status(
        #     ProcessStatus.CRAWLED_USER_INFO)
        if category_crawled_video_list:
            for category in category_crawled_video_list:
                crawl_config.update_status(
                    category['category_slug'], ProcessStatus.CRAWLING_DETAILS_VIDEO)
                video_urls = [video['url'] for video in self.load_trend_videos_crawled_by_category(
                    category['category_slug'])]
                # Split video_urls into chunks of 10 or fewer items
                chunks = [video_urls[i:i + 12]
                          for i in range(0, len(video_urls), 12)]
                for chunk in chunks:
                    self.detail_scraper.scrape_multiple_videos(
                        chunk, enable_comment=True)

                crawl_config.update_status(
                    category['category_slug'], ProcessStatus.FINISH)
        self.compressor.compress_all_folders()
        # run_sync_script()


def my_task():
    crawler = TikTokCrawlerMain()
    crawler.run()
    hcm_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time_hcm = datetime.now(hcm_tz).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Task executed at {current_time_hcm} (HCM Time Zone)")


# if __name__ == "__main__":
#     scheduler = HourlyScheduler(3600 + 1800, my_task)
#     scheduler.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         scheduler.stop()
