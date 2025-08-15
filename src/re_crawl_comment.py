import pandas as pd
from crawler.tiktok_video_details import TikTokVideoDetailScraper

# Read CSV file and extract video URLs
csv_file = "./v_daily_trending_analysis_202508152337.csv"
df = pd.read_csv(csv_file)

# Get unique video URLs from the CSV
video_urls = df['video_url'].unique().tolist()

# Split URLs into chunks of 5
chunk_size = 5
url_chunks = [video_urls[i:i + chunk_size]
              for i in range(0, len(video_urls), chunk_size)]

print(f"Total videos: {len(video_urls)}")
print(f"Processing in {len(url_chunks)} chunks of {chunk_size} videos each")

# Initialize scraper
details = TikTokVideoDetailScraper(
    base_dir="./recrawl",
    output_file="video_info_details_recrawl.csv"
)

# Process each chunk
for i, chunk in enumerate(url_chunks, 1):
    print(f"\nProcessing chunk {i}/{len(url_chunks)} ({len(chunk)} videos)")
    details.scrape_multiple_videos(
        chunk,
        enable_comment=True
    )
    print(f"Completed chunk {i}")

print("\nAll chunks processed successfully!")
