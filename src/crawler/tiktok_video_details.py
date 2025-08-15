# Explore TikTok new feed
# Get category from new feed, savem them to csv (pd), raw_data/category.csv

# div tag <div id="category-list-container" class="css-c3e3es-DivCategoryListContainer e13i6o242"><div class="css-1wvr0tq-DivArrowContainer e13i6o2410"><div class="css-1pi6qhe-DivArrowIconContainer e13i6o2411"><div class="css-1yt583-DivChevron e13i6o2412"><svg fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" class="flip-rtl "><path d="M39.88 24 26.7 10.83a1 1 0 0 1 0-1.41l2.83-2.83a1 1 0 0 1 1.41 0L47.3 22.94a1.5 1.5 0 0 1 0 2.12L30.95 41.42a1 1 0 0 1-1.41 0l-2.83-2.83a1 1 0 0 1 0-1.42L39.88 24Z"></path></svg></div></div><div class="css-f1lgvc-DivShadow e13i6o2413"></div></div><div class="css-18rvvma-DivCategoryList e13i6o240"><button class="css-189kgrc-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">All</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Singing &amp; Dancing</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Comedy</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Sports</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Anime &amp; Comics</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Relationship</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Shows</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Lipsync</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Daily Life</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Beauty Care</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Games</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Society</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Outfit</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Cars</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Food</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Animals</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Family</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Drama</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Fitness &amp; Health</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Education</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Technology</span></button></div></div>

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
# ?is_from_webapp=1&lang=eng


class TikTokVideoDetailScraper:
    def __init__(self, base_dir="raw_data/tiktok", output_file="video_info_details.csv"):
        self.output_file = output_file
        self.base_dir = base_dir
        self.seen_items = set()
        self.all_video_info = []

    def setup_browser(self, profile_dir="./browser_profile", load_previous_session=True):
        """Setup browser with persistent profile and session/cookie persistence"""
        self.browser = RealBrowser(profile_dir=profile_dir)
        driver = self.browser.setup_browser(
            load_previous_session=load_previous_session)
        return driver

    def save_video_info(self, video_info, video_url):
        os.makedirs(self.base_dir, exist_ok=True)
        file_path = os.path.join(self.base_dir, self.output_file)

        # Add video_url to the video_info dictionary
        video_info["video_url"] = video_url

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

    def save_comments(self, comments, output_file="comments.csv"):
        if not comments:
            print("No comments to save")
            return

        os.makedirs(self.base_dir, exist_ok=True)
        file_path = os.path.join(self.base_dir, output_file)

        # Check if the file exists and has content
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                # Read existing data
                existing_df = pd.read_csv(file_path)
                # Convert new comments to DataFrame
                new_df = pd.DataFrame(comments)
                # Append new data to existing data
                combined_df = pd.concat(
                    [existing_df, new_df], ignore_index=True)
            except pd.errors.EmptyDataError:
                # Handle empty file case
                print(
                    f"Warning: {file_path} exists but is empty, creating new file")
                combined_df = pd.DataFrame(comments)
            except Exception as e:
                print(f"Error reading existing file: {e}, creating new file")
                combined_df = pd.DataFrame(comments)
        else:
            # Create a new DataFrame if file doesn't exist or is empty
            combined_df = pd.DataFrame(comments)

        # Save the combined data back to the CSV file
        combined_df.to_csv(file_path, index=False)
        print(f"Appended {len(comments)} comment(s) to {file_path}")

    def extract_detail_page_info(self, driver, video_url):
        video_url = video_url + '?is_from_webapp=1&lang=eng'
        driver.get(video_url)
        time.sleep(4)  # Allow time for the page to load

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract author information
        author_container = soup.find(
            "div", class_=lambda x: x and "DivAuthorContainer" in x)
        author_info = {
            "username": author_container.find("span", class_=lambda x: x and "SpanUniqueId" in x).get_text(strip=True) if author_container else None,
            "nickname": author_container.find("span", class_=lambda x: x and "SpanNickName" in x).get_text(strip=True) if author_container else None,
        }

        # Extract video description and hashtags
        description_container = soup.find(
            "div", class_=lambda x: x and "DivDescriptionContentContainer" in x)
        description = description_container.find("span", attrs={
                                                 "data-e2e": "new-desc-span"}).get_text(strip=True) if description_container else None
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
        action_bar_container = soup.find(
            "div", class_=lambda x: x and "DivActionBarWrapper" in x)
        engagement_info = {
            "likes": action_bar_container.find("strong", attrs={"data-e2e": "like-count"}).get_text(strip=True) if action_bar_container.find("strong", attrs={"data-e2e": "like-count"}) else None,
            "comments": action_bar_container.find("strong", attrs={"data-e2e": "comment-count"}).get_text(strip=True) if action_bar_container.find("strong", attrs={"data-e2e": "comment-count"}) else None,
            "shares": action_bar_container.find("strong", attrs={"data-e2e": "share-count"}).get_text(strip=True) if action_bar_container.find("strong", attrs={"data-e2e": "share-count"}) else None,
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
            driver.execute_script(
                "var element = document.querySelector('.css-1czmy9n-DivVideoList.ege8lhx7'); if (element) element.remove();")
        except Exception as e:
            print(f"Error removing element from DOM: {e}")

        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new comments to load
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def expand_all_replies(self, driver):
        """Expand all nested replies by clicking 'View More Replies' buttons."""
        while True:
            try:
                view_more_buttons = driver.find_elements(
                    By.XPATH, "//div[contains(@class, 'DivViewRepliesContainer')]//span[contains(text(), 'View')]")

                if not view_more_buttons:
                    break
                for button in view_more_buttons:
                    ActionChains(driver).move_to_element(
                        button).click(button).perform()
                    time.sleep(1)  # Allow replies to load
            except Exception as e:
                print(f"Error expanding replies: {e}")
                break

    def extract_user_info(self, container):
        """Extract user information from a comment container."""
        try:
            user_link = container.find("a", class_="link-a11y-focus")
            username = user_link.get("href", "").lstrip(
                "/") if user_link else None
            avatar_img = container.find("img", class_="css-1zpj2q-ImgAvatar")
            avatar_url = avatar_img.get("src", None) if avatar_img else None
            return {
                "username": username,
                "avatar_url": avatar_url
            }
        except Exception as e:
            print(f"Error extracting user info: {e}")
            return None

    def extract_comments(self, driver, video_url):
        """Scroll to the bottom of the page and extract all comments and replies."""
        # Add human-like behavior before scrolling to comments
        time.sleep(3)

        # Simulate user interaction - scroll slowly to comments section
        driver.execute_script("window.scrollBy(0, window.innerHeight * 0.5);")
        time.sleep(3)

        # Try to find comments with retry logic
        max_retries = 1
        for attempt in range(max_retries):
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "[data-e2e='comment-level-1']"))
                )
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(
                        f"Attempt {attempt + 1} failed to load comments, retrying...")
                    # Refresh the page and try again
                    driver.refresh()
                    time.sleep(3)
                    continue
                else:
                    print(
                        f"Failed to load comments after {max_retries} attempts: {e}")
                    return []

        soup = BeautifulSoup(driver.page_source, "html.parser")
        comments = []
        comment_containers = soup.find_all(
            "div", class_=lambda x: x and "DivCommentObjectWrapper" in x)

        if not comment_containers:
            print("No comment containers found")
            return []

        for container in comment_containers:
            try:
                user_info = self.extract_user_info(container)

                # Look for comment content with multiple selectors
                content_element = (
                    container.find("span", attrs={"data-e2e": "comment-level-1"}) or
                    container.find("span", class_=lambda x: x and "SpanText" in x) or
                    container.find(
                        "p", class_=lambda x: x and "comment" in str(x).lower())
                )
                content = content_element.get_text(
                    strip=True) if content_element else "No content"

                # Extract likes with fallback
                likes_element = container.find(
                    "div", class_=lambda x: x and "DivLikeContainer" in x)
                likes = "0"
                if likes_element:
                    likes_span = likes_element.find("span")
                    likes = likes_span.get_text(
                        strip=True) if likes_span else "0"

                # Extract timestamp
                timestamp_element = container.find(
                    "span", class_=lambda x: x and "TUXText--weight-normal" in x)
                timestamp = timestamp_element.get_text(
                    strip=True) if timestamp_element else "No timestamp"

                # Extract parent comment if available
                parent_comment = container.find(
                    "span", attrs={"data-e2e": "comment-level-0"})
                parent_content = parent_comment.get_text(
                    strip=True) if parent_comment else None

                comments.append({
                    "username": user_info["username"] if user_info else "Unknown",
                    "avatar_url": user_info["avatar_url"] if user_info else None,
                    "content": content,
                    "likes": likes,
                    "timestamp": timestamp,
                    # "timestamp": DataCleaning.convert_text_date_to_time_stamp(timestamp),
                    "parent_comment": parent_content,
                    "video_url": video_url
                })
            except Exception as e:
                print(f"Error extracting comment: {e}")
                continue
        return comments

    def scrape_comments(self, driver):
        """Main function to scroll, expand replies, and extract comments."""
        self.scroll_to_bottom(driver)
        self.expand_all_replies(driver)
        comments = self.extract_comments(driver)
        return comments

    def scrape_detail_page_single(self, driver, video_url):
        """Scrape a single video detail page without driver management."""
        try:
            video_info = self.extract_detail_page_info(driver, video_url)
            self.save_video_info(video_info, video_url)
            print(f"Successfully scraped: {video_url}")
        except Exception as e:
            print(f"Error scraping detail page {video_url}: {e}")

    def scrape_multiple_videos(self, video_urls, profile_dir="./browser_profile", enable_comment=False, max_tabs=5):
        """
        Scrape multiple video URLs by opening them in multiple tabs first, then loop back to crawl details.
        This improves performance by parallelizing page loads.
        """
        if not video_urls:
            print("No video URLs provided")
            return

        driver = self.setup_browser(
            profile_dir=profile_dir, load_previous_session=True)
        browser = self.browser
        try:
            for i, video_url in enumerate(video_urls):
                try:
                    # Navigate to each video URL in the same tab
                    browser.open_new_tab(
                        video_url + '?is_from_webapp=1&lang=eng', )
                    print(
                        f"Processing video {i+1}/{len(video_urls)}: {video_url}")
                    time.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    author_container = soup.find(
                        "div", class_=lambda x: x and "DivAuthorContainer" in x)
                    author_info = {
                        "username": author_container.find("span", class_=lambda x: x and "SpanUniqueId" in x).get_text(strip=True) if author_container else None,
                        "nickname": author_container.find("span", class_=lambda x: x and "SpanNickName" in x).get_text(strip=True) if author_container else None,
                    }
                    time_posted_container = soup.find(
                        "span", attrs={"data-e2e": "browser-nickname"})
                    time_posted = time_posted_container.find_all(
                        "span")[-1].get_text(strip=True) if time_posted_container else None
                    description_container = soup.find(
                        "div", class_=lambda x: x and "DivDescriptionContentContainer" in x)
                    description = description_container.find("span", attrs={
                                                             "data-e2e": "new-desc-span"}).get_text(strip=True) if description_container else None
                    hashtags = [tag.get_text(strip=True) for tag in description_container.find_all(
                        "a", attrs={"data-e2e": "search-common-link"})] if description_container else []
                    music_container = soup.find(
                        "h4", attrs={"data-e2e": "browse-music"})
                    music_info = {
                        "title": music_container.find("div", class_=lambda x: x and "DivMusicText" in x).get_text(strip=True) if music_container else None,
                        "link": music_container.find("a")["href"] if music_container and music_container.find("a") else None
                    }
                    action_bar_container = soup.find(
                        "div", class_=lambda x: x and "DivActionBarWrapper" in x)
                    engagement_info = {
                        "likes": action_bar_container.find("strong", attrs={"data-e2e": "like-count"}).get_text(strip=True) if action_bar_container and action_bar_container.find("strong", attrs={"data-e2e": "like-count"}) else None,
                        "comments": action_bar_container.find("strong", attrs={"data-e2e": "comment-count"}).get_text(strip=True) if action_bar_container and action_bar_container.find("strong", attrs={"data-e2e": "comment-count"}) else None,
                        "shares": action_bar_container.find("strong", attrs={"data-e2e": "share-count"}).get_text(strip=True) if action_bar_container and action_bar_container.find("strong", attrs={"data-e2e": "share-count"}) else None,
                    }
                    video_info = {
                        "author": author_info,
                        "time_published": time_posted,
                        "description": description,
                        "hashtags": hashtags,
                        "music": music_info,
                        "engagement": engagement_info
                    }
                    self.save_video_info(video_info, video_url)
                    print(f"Successfully processed video details: {video_url}")

                    # Extract comments for each video after details

                    if enable_comment == True:
                        print(f"Extracting comments for: {video_url}")
                        browser.navigate_and_save_cookies(
                            video_url + '?is_from_webapp=1&lang=eng&lang=vi')
                        time.sleep(3.5)
                        comments = self.extract_comments(driver, video_url)
                        if comments:
                            self.save_comments(comments)
                            print(
                                f"Successfully extracted {len(comments)} comments from {video_url}")
                        else:
                            print(f"No comments found for {video_url}")
                    time.sleep(2)
                except Exception as e:
                    print(f"Error processing video {video_url}: {e}")
                    continue

            browser.save_session_info()
            browser.save_cookies()
        except Exception as e:
            print(f"Error in scrape_multiple_videos: {e}")
        finally:
            browser.quit_browser(save_session=True)
            print(f"Completed scraping {len(video_urls)} videos")

    def scrape_detail_page(self, driver, video_url):
        """Original method - now handles single video with driver management for backward compatibility."""
        if not driver:
            driver = self.setup_browser()
        try:
            self.scrape_detail_page_single(driver, video_url)
        except Exception as e:
            print(f"Error scraping detail page: {e}")
        finally:
            driver.quit()
