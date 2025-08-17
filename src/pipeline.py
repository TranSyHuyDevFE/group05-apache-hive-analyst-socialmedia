
# Flow xu ly crawller va report theo ngay
'''
1. Crawller du lieu tu cac trang web ve
2. Lam sach du lieu & luu vao folder clearned_data
3. Chay nhan dien tich cuc tieu cuc
4. Sync file qua hive
'''
import time
from crawler.scheduler import HourlyScheduler
from crawler.tiktok_crawller_main import TikTokCrawlerMain
from data_preprocessing.main_process_details_vid import MainProcessDetailsVid
from data_preprocessing.main_process_related_videos import MainProcessRelatedVideos
from data_preprocessing.main_process_trend_videos import MainProcessTrendVideos
from data_preprocessing.main_process_comments import MainProcessComments
from data_preprocessing.main_process_user_details import MainProcessUserDetails
from data_preprocessing.file_path import FilePaths

from sentiment.main import SentimentProcessing
import subprocess
DATA_CRAWLLED_DIRECTORY = "./data/raw_data/tiktok"
CLEANED_DATA_DIRECTORY = "./data/cleaned_data/"


def scrapper_process():
    """
    Scrapper process.
    """
    craller = TikTokCrawlerMain()
    # Assuming run method starts the crawling process
    craller.run()
    print("Scrapper process started...")
    # Here you would implement the actual scrapping logic


def clean_data_process():
    """
    Clean data process.
    """
    main_process_video = MainProcessDetailsVid(
        FilePaths(
            input_path=f"{DATA_CRAWLLED_DIRECTORY}/details_video_info.csv",
            output_path=f'{CLEANED_DATA_DIRECTORY}/video_info_details'
        )
    )
    main_process_video.run()
    # main_process_related_videos = MainProcessRelatedVideos(
    #     FilePaths(
    #         input_path=f"{DATA_CRAWLLED_DIRECTORY}/related_videos.csv",
    #         output_path=f'{CLEANED_DATA_DIRECTORY}/related_videos'
    #     )
    # )
    # main_process_related_videos.run()
    main_process_trend_videos = MainProcessTrendVideos(
        FilePaths(
            input_path=f"{DATA_CRAWLLED_DIRECTORY}/trend_videos.csv",
            output_path=f'{CLEANED_DATA_DIRECTORY}/video'
        )
    )
    main_process_trend_videos.run()
    main_process_comments = MainProcessComments(
        FilePaths(
            input_path=f"{DATA_CRAWLLED_DIRECTORY}/comments.csv",
            output_path=f'{CLEANED_DATA_DIRECTORY}/comments'
        )
    )
    main_process_comments.run()
    # main_process_user_details = MainProcessUserDetails(
    #     FilePaths(
    #         input_path=f"{DATA_CRAWLLED_DIRECTORY}/user_info.csv",
    #         output_path=f'{CLEANED_DATA_DIRECTORY}/user_info_details'
    #     )
    # )
    # main_process_user_details.run()
    print("Clean data process started...")


def sentiment_analysis_process():
    """
    Sentiment analysis process.
    """
    print("Syncing data to Hive process started...")
    s = SentimentProcessing(
        input_dir=f"{CLEANED_DATA_DIRECTORY}/comments",
        output_dir=f"{CLEANED_DATA_DIRECTORY}/comments",
    )
    s.run()
    print("Sentiment analysis process started...")


def sync_data_to_hive_process():
    """
    Sync data to Hive process.
    """
    try:
        result = subprocess.run(
            ["./scripts/excute-run-docker.sh"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Sync to Hive output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error syncing to Hive:", e.stderr)


def clean_up():
    """
    move:    -  data/cleaned_data -> data/cleaned_data_bk_<timestamp> 
    remove: - data/crawled_data
    """
    print("Cleaning up...")
    subprocess.run(["mv", "-f", CLEANED_DATA_DIRECTORY,
                   f"data/cleaned_data_bk_{int(time.time())}"])
    subprocess.run(["rm", "-rf", DATA_CRAWLLED_DIRECTORY])
    print("Cleanup completed.")


def main():
    scrapper_process()
    clean_data_process()
    sentiment_analysis_process()
    # sync_data_to_hive_process()
    clean_up()


if __name__ == "__main__":
    scheduler = HourlyScheduler(3600 + 1800, main)
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
