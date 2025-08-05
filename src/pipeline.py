
# Flow xu ly crawller va report theo ngay
'''
1. Crawller du lieu tu cac trang web ve
2. Lam sach du lieu & luu vao folder clearned_data
3. Chay nhan dien tich cuc tieu cuc
4. Sync file qua hive
'''
from crawler.tiktok_crawller_main import TikTokCrawlerMain

def scrapper_process():
    """
    Scrapper process.
    """
    craller = TikTokCrawlerMain()
    craller.run()  # Assuming run method starts the crawling process
    print("Scrapper process started...")
    # Here you would implement the actual scrapping logic
    pass
def clean_data_process():
    """
    Clean data process.
    """
    print("Clean data process started...")
    
def sentiment_analysis_process():
    """
    Sentiment analysis process.
    """
    print("Sentiment analysis process started...")
    
# Sync data qua hive
def sync_data_to_hive_process():
    """
    Sync data to Hive process.
    """
    print("Syncing data to Hive process started...")
    # Here you would implement the actual sync logic
    pass
def main():
    scrapper_process()
    clean_data_process()
    sentiment_analysis_process()
    sync_data_to_hive_process()

if __name__ == "__main__":
    main()