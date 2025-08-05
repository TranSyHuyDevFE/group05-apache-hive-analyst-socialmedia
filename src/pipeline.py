
# Flow xu ly crawller va report theo ngay
'''
1. Crawller du lieu tu cac trang web ve
2. Lam sach du lieu & luu vao folder clearned_data
3. Chay nhan dien tich cuc tieu cuc
4. Sync file qua hive
'''
from crawler.tiktok_crawller_main import TikTokCrawlerMain
from data_preprocessing.main_process_details_vid import MainProcessDetailsVid
from data_preprocessing.main_process_related_videos import MainProcessRelatedVideos
from data_preprocessing.main_process_trend_videos import MainProcessTrendVideos
from data_preprocessing.main_process_comments import MainProcessComments
from data_preprocessing.main_process_user_details import MainProcessUserDetails
from data_preprocessing.file_path import FilePaths

DATA_CRAWLLED_DIRECTORY = "./data/raw_data/tiktok"

def scrapper_process():
    """
    Scrapper process.
    """
    craller = TikTokCrawlerMain()
    craller.run()  # Assuming run method starts the crawling process
    print("Scrapper process started...")
    # Here you would implement the actual scrapping logic


def clean_data_process():
    """
    Clean data process.
    """
    main_process_video = MainProcessDetailsVid(
        FilePaths(
            input_path=f"{DATA_CRAWLLED_DIRECTORY}/details_video_info.csv",
            output_path="./cleaned_data"
        )
    )
    main_process_video.run()
    main_process_related_videos = MainProcessRelatedVideos(
        FilePaths(
            input_path=f"{DATA_CRAWLLED_DIRECTORY}/related_videos.csv",
            output_path="./cleaned_data"
        )
    )
    main_process_related_videos.run()
    main_process_trend_videos = MainProcessTrendVideos(
        FilePaths(
            input_path=f"{DATA_CRAWLLED_DIRECTORY}/trend_videos.csv",
            output_path="./cleaned_data"
        )
    )
    main_process_trend_videos.run()
    main_process_comments = MainProcessComments(
        FilePaths(
            input_path=f"{DATA_CRAWLLED_DIRECTORY}/comments.csv",
            output_path="./cleaned_data"
        )
    )
    main_process_comments.run()
    main_process_user_details = MainProcessUserDetails(
        FilePaths(
            input_path=f"{DATA_CRAWLLED_DIRECTORY}/user_info.csv",
            output_path="./cleaned_data"
        )
    )
    main_process_user_details.run()
    # Assuming these methods handle the cleaning and saving of data
    # Here you would implement the actual cleaning logic
    # For example, you might read the raw data, process it, and save it to a cleaned directory
    # This is a placeholder for the actual cleaning logic
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
