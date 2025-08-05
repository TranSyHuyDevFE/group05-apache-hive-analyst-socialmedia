# Explore TikTok new feed
## Get category from new feed, savem them to csv (pd), raw_data/category.csv

## div tag <div id="category-list-container" class="css-c3e3es-DivCategoryListContainer e13i6o242"><div class="css-1wvr0tq-DivArrowContainer e13i6o2410"><div class="css-1pi6qhe-DivArrowIconContainer e13i6o2411"><div class="css-1yt583-DivChevron e13i6o2412"><svg fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" class="flip-rtl "><path d="M39.88 24 26.7 10.83a1 1 0 0 1 0-1.41l2.83-2.83a1 1 0 0 1 1.41 0L47.3 22.94a1.5 1.5 0 0 1 0 2.12L30.95 41.42a1 1 0 0 1-1.41 0l-2.83-2.83a1 1 0 0 1 0-1.42L39.88 24Z"></path></svg></div></div><div class="css-f1lgvc-DivShadow e13i6o2413"></div></div><div class="css-18rvvma-DivCategoryList e13i6o240"><button class="css-189kgrc-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">All</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Singing &amp; Dancing</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Comedy</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Sports</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Anime &amp; Comics</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Relationship</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Shows</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Lipsync</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Daily Life</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Beauty Care</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Games</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Society</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Outfit</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Cars</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Food</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Animals</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Family</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Drama</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Fitness &amp; Health</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Education</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Technology</span></button></div></div>

import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .browser_setup import RealBrowser
from selenium.webdriver.common.action_chains import ActionChains
import json
# ?is_from_webapp=1
class TikTokVideoRelatedScraper:
    def __init__(self, base_dir="raw_data/tiktok", output_file="video_info_details.csv"):
        self.output_file = output_file
        self.base_dir = base_dir
        self.seen_items = set()
        self.all_video_info = []

    def setup_browser(self):
        browser = RealBrowser()
        return browser.setup_browser()

    def save_video_info(self, video_info):
        os.makedirs(self.base_dir, exist_ok=True)
        file_path = os.path.join(self.base_dir, self.output_file)

        # Check if the file exists
        if os.path.exists(file_path):
            # Read existing data
            existing_df = pd.read_csv(file_path)
            # Convert new video info to DataFrame
            new_df = pd.DataFrame([video_info])
            # Append new data to existing data
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            # Create a new DataFrame if file doesn't exist
            combined_df = pd.DataFrame([video_info])

        # Save the combined data back to the CSV file
        combined_df.to_csv(file_path, index=False)
        print(f"Appended {len([video_info])} video(s) to {file_path}")

    
    def scrape_related_videos(self, video_url, max_time=15):
        driver = self.setup_browser()
        try:
            driver.get(video_url)
            time.sleep(4)  # Allow time for the page to load

            # Remove the specified element from the DOM
            try:
                driver.execute_script("var element = document.querySelector('.css-7whb78-DivCommentListContainer.e10noszu0'); if (element) element.remove();")
            except Exception as e:
                print(f"Error removing element from DOM: {e}")

            related_videos = []
            last_height = driver.execute_script("return document.body.scrollHeight")

            start_time = time.time()  # Record the start time

            while True:
                # Check if the elapsed time exceeds the maximum time
                elapsed_time = time.time() - start_time
                if elapsed_time > max_time:
                    print("Time limit reached. Saving collected data and stopping.")
                    break

                # Scroll to the bottom of the page
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for new videos to load

                # Parse the page source
                soup = BeautifulSoup(driver.page_source, "html.parser")
                video_containers = soup.find_all("div", class_=lambda x: x and "css-fxdm8v-DivItemContainer" in x)

                for container in video_containers:
                    try:
                        title = container.find("div", class_=lambda x: x and "DivTitle" in x).get_text(strip=True)
                        author = container.find("span", class_=lambda x: x and "SpanUniqueId" in x).get_text(strip=True)
                        likes = container.find("div", class_=lambda x: x and "DivLikeInfo" in x).get_text(strip=True)
                        video_link = container.find("a")['href']

                        related_videos.append({
                            "video_link": video_link,
                            "parrent_video_url": video_url,
                            "title": title,
                            "author": author,
                            "likes": likes,
                        })
                    except Exception as e:
                        print(f"Error extracting related video: {e}")

                # Check if the page height has stopped increasing
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Save related videos to a CSV file
            related_videos_file_path = os.path.join(self.base_dir, "related_videos.csv")
            related_videos_df = pd.DataFrame(related_videos)
            related_videos_df.to_csv(related_videos_file_path, index=False, encoding="utf-8")
            print(f"Extracted {len(related_videos)} related videos and saved to {related_videos_file_path}")
        except Exception as e:
            print(f"Error scraping related videos: {e}")
        finally:
            driver.quit()
if __name__ == "__main__":
    scraper = TikTokVideoRelatedScraper()
    scraper.scrape_related_videos('https://www.tiktok.com/@sau.drama/video/7522016067275820309')
