# Viet fiel crawl cho nay
import sys
import os

# Append parent directory to sys.path
from crawler.tiktok_crawller_main import TikTokCrawlerMain

def crawller_process():
    """
   
    """
    print("Crawling process started...")
    try:
        crawler = TikTokCrawlerMain()
        crawler.run()
    except Exception as e:
        print(f"An error occurred during the crawling process: {e}")
        