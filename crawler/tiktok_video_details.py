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
from selenium.webdriver.common.action_chains import ActionChains
import json
# ?is_from_webapp=1
class TikTokVideoDetailScraper:
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

    def extract_detail_page_info(self, driver, video_url):
        video_url = video_url + '?is_from_webapp=1'
        driver.get(video_url)
        time.sleep(4)  # Allow time for the page to load

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract author information
        author_container = soup.find("div", class_=lambda x: x and "DivAuthorContainer" in x)
        author_info = {
            "username": author_container.find("span", class_=lambda x: x and "SpanUniqueId" in x).get_text(strip=True) if author_container else None,
            "nickname": author_container.find("span", class_=lambda x: x and "SpanNickName" in x).get_text(strip=True) if author_container else None,
        }

        # Extract video description and hashtags
        description_container = soup.find("div", class_=lambda x: x and "DivDescriptionContentContainer" in x)
        description = description_container.find("span", attrs={"data-e2e": "new-desc-span"}).get_text(strip=True) if description_container else None
        hashtags = [
            tag.get_text(strip=True) for tag in description_container.find_all("strong", class_=lambda x: x and "css-1qkxi8e-StrongText" in x)
        ] if description_container else []

        # Extract music information
        music_container = soup.find("h4", attrs={"data-e2e": "browse-music"})
        music_info = {
            "title": music_container.find("div", class_=lambda x: x and "DivMusicText" in x).get_text(strip=True) if music_container else None,
            "link": music_container.find("a")["href"] if music_container and music_container.find("a") else None
        }

        # Extract likes, comments, shares, and video link from the new container
        action_bar_container = soup.find("div", class_=lambda x: x and "DivActionBarWrapper" in x)
        engagement_info = {
            "likes": action_bar_container.find("strong", attrs={"data-e2e": "like-count"}).get_text(strip=True) if action_bar_container.find("strong", attrs={"data-e2e": "like-count"}) else None,
            "comments": action_bar_container.find("strong", attrs={"data-e2e": "comment-count"}).get_text(strip=True) if action_bar_container.find("strong", attrs={"data-e2e": "comment-count"}) else None,
            "shares": action_bar_container.find("strong", attrs={"data-e2e": "share-count"}).get_text(strip=True) if action_bar_container.find("strong", attrs={"data-e2e": "share-count"}) else None,
            "video_link": soup.find("p", attrs={"data-e2e": "browse-video-link"}).get_text(strip=True) if soup.find("p", attrs={"data-e2e": "browse-video-link"}) else None
        }

        return {
            "author": author_info,
            "description": description,
            "hashtags": hashtags,
            "music": music_info,
            "engagement": engagement_info
        }


    def scroll_to_bottom(self, driver):
        """Scroll to the bottom of the page to load all comments."""
        # Remove the specified element from the DOM
        try:
            driver.execute_script("var element = document.querySelector('.css-1czmy9n-DivVideoList.ege8lhx7'); if (element) element.remove();")
        except Exception as e:
            print(f"Error removing element from DOM: {e}")

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new comments to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def expand_all_replies(self, driver):
        """Expand all nested replies by clicking 'View More Replies' buttons."""
        while True:
            try:
                view_more_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'DivViewRepliesContainer')]//span[contains(text(), 'View')]")
                
                if not view_more_buttons:
                    break
                for button in view_more_buttons:
                    ActionChains(driver).move_to_element(button).click(button).perform()
                    time.sleep(1)  # Allow replies to load
            except Exception as e:
                print(f"Error expanding replies: {e}")
                break

    def extract_user_info(self, container):
        """Extract user information from a comment container."""
        try:
            user_link = container.find("a", class_="link-a11y-focus")
            username = user_link.get("href", "").lstrip("/") if user_link else None
            avatar_img = container.find("img", class_="css-1zpj2q-ImgAvatar")
            avatar_url = avatar_img.get("src", None) if avatar_img else None
            return {
                "username": username,
                "avatar_url": avatar_url
            }
        except Exception as e:
            print(f"Error extracting user info: {e}")
            return None

    def extract_comments(self, driver):
        """Extract all comments and replies from the page."""
        soup = BeautifulSoup(driver.page_source, "html.parser")
        comments = []
        comment_containers = soup.find_all("div", class_=lambda x: x and "DivCommentObjectWrapper" in x)
        for container in comment_containers:
            try:
                user_info = self.extract_user_info(container)
                content = container.find("span", attrs={"data-e2e": "comment-level-1"}).get_text(strip=True)
                likes = container.find("div", class_=lambda x: x and "DivLikeContainer" in x).find("span").get_text(strip=True)
                timestamp = container.find("span", class_=lambda x: x and "TUXText--weight-normal" in x).get_text(strip=True)

                # Extract parent comment if available
                parent_comment = container.find("span", attrs={"data-e2e": "comment-level-0"})
                parent_content = parent_comment.get_text(strip=True) if parent_comment else None

                comments.append({
                    "user_info": user_info,
                    "content": content,
                    "likes": likes,
                    "timestamp": timestamp,
                    "parent_comment": parent_content
                })
            except Exception as e:
                print(f"Error extracting comment: {e}")
        return comments

    def scrape_comments(self, driver):
        """Main function to scroll, expand replies, and extract comments."""
        self.scroll_to_bottom(driver)
        self.expand_all_replies(driver)
        comments = self.extract_comments(driver)
        return comments

    def scrape_detail_page(self, video_url):
        driver = self.setup_browser()
        try:
            video_info = self.extract_detail_page_info(driver, video_url)
            self.save_video_info(video_info)
            time.sleep(2)  # Allow time for the page to load

            # Scroll to load all comments
            self.scroll_to_bottom(driver)
            time.sleep(2)  # Allow time for the page to load

            # Expand all replies
            self.expand_all_replies(driver)
            time.sleep(2)  # Allow time for the page to load
            # Extract comments and replies
            comments = self.extract_comments(driver)

            # Add video_url to each comment
            for comment in comments:
                comment["video_url"] = video_url

            # Save comments to a CSV file
            comments_file_path = os.path.join(self.base_dir, f"comments/{video_url.split('/')[-1]}.csv")
            comments_df = pd.DataFrame(comments)
            comments_df.to_csv(comments_file_path, index=False, encoding="utf-8")
            print(f"Extracted {len(comments)} comments and saved to {comments_file_path}")
        except Exception as e:
            print(f"Error scraping detail page: {e}")
        finally:
            driver.quit()
if __name__ == "__main__":
    scraper = TikTokVideoDetailScraper()
    scraper.scrape_detail_page('https://www.tiktok.com/@sau.drama/video/7522016067275820309')
