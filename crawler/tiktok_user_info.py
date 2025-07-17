# Explore TikTok new feed
# Get category from new feed, savem them to csv (pd), raw_data/category.csv

# div tag <div id="category-list-container" class="css-c3e3es-DivCategoryListContainer e13i6o242"><div class="css-1wvr0tq-DivArrowContainer e13i6o2410"><div class="css-1pi6qhe-DivArrowIconContainer e13i6o2411"><div class="css-1yt583-DivChevron e13i6o2412"><svg fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" class="flip-rtl "><path d="M39.88 24 26.7 10.83a1 1 0 0 1 0-1.41l2.83-2.83a1 1 0 0 1 1.41 0L47.3 22.94a1.5 1.5 0 0 1 0 2.12L30.95 41.42a1 1 0 0 1-1.41 0l-2.83-2.83a1 1 0 0 1 0-1.42L39.88 24Z"></path></svg></div></div><div class="css-f1lgvc-DivShadow e13i6o2413"></div></div><div class="css-18rvvma-DivCategoryList e13i6o240"><button class="css-189kgrc-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">All</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Singing &amp; Dancing</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Comedy</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Sports</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Anime &amp; Comics</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Relationship</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Shows</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Lipsync</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Daily Life</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Beauty Care</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Games</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Society</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Outfit</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Cars</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Food</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Animals</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Family</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Drama</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Fitness &amp; Health</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Education</span></button><button class="css-qexeba-ButtonCategoryItemContainer e13i6o248"><span class="css-3pue8b-SpanCategoryName e13i6o249">Technology</span></button></div></div>

import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from tiktok_data_clearning import DataCleaning
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser_setup import RealBrowser
from selenium.webdriver.common.action_chains import ActionChains


class TikTokUserInfoScraper:
    def __init__(self, base_dir="raw_data/tiktok", output_file="user_info.csv"):
        self.output_file = output_file
        self.base_dir = base_dir
        self.seen_users = set()
        self.all_user_info = []

    def setup_browser(self):
        browser = RealBrowser()
        return browser.setup_browser()

    def save_user_info(self, user_info, username):
        os.makedirs(self.base_dir, exist_ok=True)
        file_path = os.path.join(self.base_dir, self.output_file)

        # Add username to the user_info dictionary
        user_info["username"] = username

        # Check if the file exists
        if os.path.exists(file_path):
            # Read existing data
            existing_df = pd.read_csv(file_path)
            # Convert new user info to DataFrame
            new_df = pd.DataFrame([user_info])
            # Append new data to existing data
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            # Create a new DataFrame if file doesn't exist
            combined_df = pd.DataFrame([user_info])

        # Save the combined data back to the CSV file
        combined_df.to_csv(file_path, index=False)
        print(f"Appended {len([user_info])} user(s) to {file_path}")

    def extract_user_page_info(self, driver, username):
        user_url = f'https://www.tiktok.com/@{username}?is_from_webapp=1'
        driver.get(user_url)
        time.sleep(4)  # Allow time for the page to load

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract user avatar
        avatar_container = soup.find("div", attrs={"data-e2e": "user-avatar"})
        avatar_url = None
        if avatar_container:
            img_tag = avatar_container.find(
                "img", class_="css-1zpj2q-ImgAvatar")
            avatar_url = img_tag.get("src") if img_tag else None

        # Extract user title and subtitle
        title_element = soup.find("h1", attrs={"data-e2e": "user-title"})
        subtitle_element = soup.find("h2", attrs={"data-e2e": "user-subtitle"})

        user_title = title_element.get_text(
            strip=True) if title_element else None
        user_subtitle = subtitle_element.get_text(
            strip=True) if subtitle_element else None

        # Extract follower counts
        following_count = soup.find(
            "strong", attrs={"data-e2e": "following-count"})
        followers_count = soup.find(
            "strong", attrs={"data-e2e": "followers-count"})
        likes_count = soup.find("strong", attrs={"data-e2e": "likes-count"})

        counts_info = {
            "following": following_count.get_text(strip=True) if following_count else None,
            "followers": followers_count.get_text(strip=True) if followers_count else None,
            "likes": likes_count.get_text(strip=True) if likes_count else None
        }

        # Clean
        counts_info = {k: DataCleaning.convert_text_to_number(
            v) for k, v in counts_info.items()}

        # Extract user bio
        bio_element = soup.find("h2", attrs={"data-e2e": "user-bio"})
        user_bio = bio_element.get_text(strip=True) if bio_element else None

        # Extract user links
        link_elements = soup.find_all("a", attrs={"data-e2e": "user-link"})
        user_links = []
        for link in link_elements:
            link_text = link.find("span", class_="css-847r2g-SpanLink")
            if link_text:
                user_links.append({
                    "url": link.get("href"),
                    "text": link_text.get_text(strip=True)
                })

        return {
            "user_title": user_title,
            "user_subtitle": user_subtitle,
            "avatar_url": avatar_url,
            "counts": counts_info,
            "bio": user_bio,
            "links": user_links
        }

    def scrape_user_page_single(self, driver, username):
        """Scrape a single user profile page without driver management."""
        try:
            user_info = self.extract_user_page_info(driver, username)
            self.save_user_info(user_info, username)
            print(f"Successfully scraped user: {username}")
        except Exception as e:
            print(f"Error scraping user page {username}: {e}")

    def scrape_multiple_users(self, usernames):
        """Scrape multiple user profiles using optimized tab strategy."""
        if not usernames:
            print("No usernames provided")
            return

        driver = self.setup_browser()
        try:
            # Phase 1: Open all tabs and load URLs
            print(f"Opening {len(usernames)} tabs...")
            tab_username_mapping = {}

            for i, username in enumerate(usernames):
                try:
                    user_url = f'https://www.tiktok.com/@{username}?is_from_webapp=1'
                    if i == 0:
                        # Use the first tab
                        driver.get(user_url)
                    else:
                        # Open new tab and navigate to URL
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.get(user_url)

                    # Map tab handle to username
                    tab_username_mapping[driver.current_window_handle] = username
                    print(f"Opened tab {i+1}/{len(usernames)}: @{username}")

                except Exception as e:
                    print(f"Error opening tab for @{username}: {e}")
                    continue

            # Small delay to let all pages start loading
            time.sleep(0.2)

            # Phase 2: Process each tab sequentially
            print("Processing tabs for data extraction...")
            for tab_handle, username in tab_username_mapping.items():
                try:
                    # Switch to the tab
                    driver.switch_to.window(tab_handle)

                    # Wait for page to load completely
                    time.sleep(0.2)

                    # Remove captcha container and modal overlays if they exist
                    try:
                        driver.execute_script("""
                            var captchaElement = document.getElementById('captcha-verify-container-main-page');
                            if (captchaElement) {
                                captchaElement.remove();
                                console.log('Captcha container removed');
                            }
                            
                            var modalOverlays = document.querySelectorAll('.TUXModal-overlay');
                            modalOverlays.forEach(function(overlay) {
                                overlay.remove();
                                console.log('TUXModal-overlay removed');
                            });
                        """)
                    except Exception as e:
                        print(
                            f"Error removing captcha container or modal overlays: {e}")

                    # Extract data using existing logic
                    soup = BeautifulSoup(driver.page_source, "html.parser")

                    # Extract user avatar
                    avatar_container = soup.find(
                        "div", attrs={"data-e2e": "user-avatar"})
                    avatar_url = None
                    if avatar_container:
                        img_tag = avatar_container.find(
                            "img", class_="css-1zpj2q-ImgAvatar")
                        avatar_url = img_tag.get("src") if img_tag else None

                    # Extract user title and subtitle
                    title_element = soup.find(
                        "h1", attrs={"data-e2e": "user-title"})
                    subtitle_element = soup.find(
                        "h2", attrs={"data-e2e": "user-subtitle"})

                    user_title = title_element.get_text(
                        strip=True) if title_element else None
                    user_subtitle = subtitle_element.get_text(
                        strip=True) if subtitle_element else None

                    # Extract follower counts
                    following_count = soup.find(
                        "strong", attrs={"data-e2e": "following-count"})
                    followers_count = soup.find(
                        "strong", attrs={"data-e2e": "followers-count"})
                    likes_count = soup.find(
                        "strong", attrs={"data-e2e": "likes-count"})

                    counts_info = {
                        "following": following_count.get_text(strip=True) if following_count else None,
                        "followers": followers_count.get_text(strip=True) if followers_count else None,
                        "likes": likes_count.get_text(strip=True) if likes_count else None
                    }

                    # Extract user bio
                    bio_element = soup.find(
                        "h2", attrs={"data-e2e": "user-bio"})
                    user_bio = bio_element.get_text(
                        strip=True) if bio_element else None

                    # Extract user links
                    link_elements = soup.find_all(
                        "a", attrs={"data-e2e": "user-link"})
                    user_links = []
                    for link in link_elements:
                        link_text = link.find(
                            "span", class_="css-847r2g-SpanLink")
                        if link_text:
                            user_links.append({
                                "url": link.get("href"),
                                "text": link_text.get_text(strip=True)
                            })

                    user_info = {
                        "user_title": user_title,
                        "user_subtitle": user_subtitle,
                        "avatar_url": avatar_url,
                        "counts": counts_info,
                        "bio": user_bio,
                        "links": user_links
                    }

                    # Save the extracted data
                    self.save_user_info(user_info, username)
                    print(f"Successfully processed user: @{username}")

                except Exception as e:
                    print(f"Error processing tab for @{username}: {e}")
                    continue

        except Exception as e:
            print(f"Error in scrape_multiple_users: {e}")
        finally:
            driver.quit()
            print(f"Completed scraping {len(usernames)} users")

    def scrape_user_page(self, driver, username):
        """Original method - now handles single user with driver management for backward compatibility."""
        if not driver:
            driver = self.setup_browser()
        try:
            self.scrape_user_page_single(driver, username)
        except Exception as e:
            print(f"Error scraping user page: {e}")
        finally:
            driver.quit()


if __name__ == "__main__":
    user_scraper = TikTokUserInfoScraper()

    # Example usage for single user
    # user_scraper.scrape_user_page(None, 'phucsyno96')

    # Example usage for multiple users
    usernames = [
        'phucsyno96',
        # Add more usernames as needed
    ]
    user_scraper.scrape_multiple_users(usernames)
