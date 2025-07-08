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
from browser_setup import RealBrowser

class TikTokVideoScraper:
    def __init__(self, base_dir="raw_data/tiktok", output_file="video_info.csv"):
        self.output_file = output_file
        self.base_dir = base_dir
        self.seen_items = set()
        self.all_video_info = []

    def setup_browser(self):
        browser = RealBrowser()
        return browser.setup_browser()

    def get_explore_items(self, driver):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        explore_items = soup.find_all("div", class_=lambda x: x and "css-10op4xt-DivContainer-StyledDivContainerV2" in x)
        return explore_items

    def extract_video_data(self, item):
        video_link = item.find("a", class_=lambda x: x and "css-1mdo0pl-AVideoContainer" in x)
        video_url = video_link['href'] if video_link else None

        if video_url and video_url not in self.seen_items:
            self.seen_items.add(video_url)
            video_data = {
                "url": video_url,
                "thumbnail": item.find("img")["src"] if item.find("img") else None,
                "description": item.find("span", attrs={"style": "box-sizing: border-box; display: block; overflow: hidden;"}).get("alt") if item.find("span", attrs={"style": "box-sizing: border-box; display: block; overflow: hidden;"}) else None,
                "likes": item.find("div", class_=lambda x: x and "css-qptaao-DivIconText" in x).find("span").get_text(strip=True) if item.find("div", class_=lambda x: x and "css-qptaao-DivIconText" in x) else None
            }
            return video_data
        return None

    def save_video_info(self):
        os.makedirs(self.base_dir, exist_ok=True)
        file_path = os.path.join(self.base_dir, self.output_file)
        df = pd.DataFrame(self.all_video_info)
        df.to_csv(file_path, index=False)
        print(f"Saved {len(self.all_video_info)} videos to {file_path}")

    def get_categories(self, driver):
        url = "https://www.tiktok.com/explore"
        driver.get(url)
        # Wait for the category list container to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "category-list-container"))
        )
        time.sleep(2)  # Give extra time for dynamic content to load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        category_container = soup.find("div", id="category-list-container")
        if not category_container:
            print("Category container not found.")
            return []

        # Find all span tags with class containing 'SpanCategoryName'
        categories = []
        for span in category_container.find_all("span", class_=lambda x: x and "SpanCategoryName" in x):
            display = span.get_text(strip=True)
            if display:
                slug = display.lower().replace("&", "and").replace("'", "").replace(".", "").replace(",", "")
                slug = "-".join(slug.split())
                categories.append({"display": display, "slug": slug})

        return categories

    def scrape_videos(self):
        url = "https://www.tiktok.com/explore"
        driver = self.setup_browser()
        try:
            driver.get(url)

            # Get categories
            categories = self.get_categories(driver)

            for category in categories:
                print(f"Switching to category: {category['display']}")
                driver.execute_script("window.scrollTo(0, 0);")  # Scroll to top
                time.sleep(5)  # Delay before clicking
                category_button = driver.find_element(By.XPATH, f"//span[text()='{category['display']}']")
                category_button.click()
                time.sleep(2)

                while True:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='explore-item']"))
                    )
                    time.sleep(2)

                    explore_items = self.get_explore_items(driver)
                    if not explore_items:
                        print("Explore items not found.")
                        break

                    for item in explore_items:
                        video_data = self.extract_video_data(item)
                        if video_data:
                            video_data['category'] = category['slug']  # Add category to video data
                            self.all_video_info.append(video_data)

                    self.save_video_info()

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                    new_explore_items = self.get_explore_items(driver)
                    new_video_urls = {
                        item.find("a", class_=lambda x: x and "css-1mdo0pl-AVideoContainer" in x)['href']
                        for item in new_explore_items if item.find("a", class_=lambda x: x and "css-1mdo0pl-AVideoContainer" in x)
                    }

                    if not new_video_urls.difference(self.seen_items):
                        print("No new items loaded. Reached the end of the page.")
                        break
        finally:
            driver.quit()

if __name__ == "__main__":
    scraper = TikTokVideoScraper()
    scraper.scrape_videos()
