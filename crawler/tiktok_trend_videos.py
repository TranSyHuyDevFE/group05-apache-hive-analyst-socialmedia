import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from tiktok_data_clearning import DataCleaning
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser_setup import RealBrowser
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class TikTokVideoScraper:
    def __init__(self, base_dir="raw_data/tiktok", output_file="video_info.csv"):
        self.output_file = output_file
        self.base_dir = base_dir
        self.seen_items = set()
        self.all_video_info = []
        self._lock = threading.Lock()
        self.tab_states = {}  # Track each tab's state

    def setup_browser(self):
        browser = RealBrowser()
        return browser.setup_browser()

    def open_category_tab(self, driver, category, tab_index):
        """Open a new tab and navigate to the specific category"""
        if tab_index > 0:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[tab_index])
        
        url = f"https://www.tiktok.com/explore"
        driver.get(url)
        
        # Wait for page to load and click on category
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "category-list-container"))
        )
        time.sleep(2)
        
        try:
            category_button = driver.find_element(By.XPATH, f"//span[text()='{category['display']}']")
            category_button.click()
            time.sleep(2)
            print(f"Tab {tab_index}: Opened category {category['display']}")
        except Exception as e:
            print(f"Tab {tab_index}: Failed to click category {category['display']}: {e}")

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
            video_data["likes"] = DataCleaning.convert_text_to_number(video_data["likes"])
            return video_data
        return None

    def save_video_info(self):
        os.makedirs(self.base_dir, exist_ok=True)
        file_path = os.path.join(self.base_dir, self.output_file)
        df = pd.DataFrame(self.all_video_info)
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
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

    def scrape_category_tab(self, driver, category, tab_index):
        """Scrape videos from a specific category tab"""
        try:
            driver.switch_to.window(driver.window_handles[tab_index])
            category_seen_items = set()
            
            while True:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='explore-item']"))
                )
                time.sleep(2)

                explore_items = self.get_explore_items(driver)
                if not explore_items:
                    print(f"Tab {tab_index}: No explore items found for {category['display']}")
                    break

                new_videos_found = False
                for item in explore_items:
                    video_data = self.extract_video_data_for_tab(item, category, category_seen_items)
                    if video_data:
                        with self._lock:
                            self.all_video_info.append(video_data)
                        new_videos_found = True

                if new_videos_found:
                    with self._lock:
                        self.save_video_info()

                # Scroll down to load more content
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

                # Check if new content loaded
                new_explore_items = self.get_explore_items(driver)
                new_video_urls = {
                    item.find("a", class_=lambda x: x and "css-1mdo0pl-AVideoContainer" in x)['href']
                    for item in new_explore_items 
                    if item.find("a", class_=lambda x: x and "css-1mdo0pl-AVideoContainer" in x)
                }

                if not new_video_urls.difference(category_seen_items):
                    print(f"Tab {tab_index}: No new items for {category['display']}. Reached end.")
                    break

        except Exception as e:
            print(f"Tab {tab_index}: Error scraping {category['display']}: {e}")

    def extract_video_data_for_tab(self, item, category, category_seen_items):
        """Extract video data with tab-specific seen items tracking"""
        video_link = item.find("a", class_=lambda x: x and "css-1mdo0pl-AVideoContainer" in x)
        video_url = video_link['href'] if video_link else None

        if video_url and video_url not in category_seen_items:
            category_seen_items.add(video_url)
            with self._lock:
                if video_url not in self.seen_items:
                    self.seen_items.add(video_url)
                    video_data = {
                        "url": video_url,
                        "thumbnail": item.find("img")["src"] if item.find("img") else None,
                        "description": item.find("span", attrs={"style": "box-sizing: border-box; display: block; overflow: hidden;"}).get("alt") if item.find("span", attrs={"style": "box-sizing: border-box; display: block; overflow: hidden;"}) else None,
                        "likes": item.find("div", class_=lambda x: x and "css-qptaao-DivIconText" in x).find("span").get_text(strip=True) if item.find("div", class_=lambda x: x and "css-qptaao-DivIconText" in x) else None,
                        "category": category['slug']
                    }
                    return video_data
        return None

    def init_tab_state(self, tab_index, category):
        """Initialize tracking state for a tab"""
        self.tab_states[tab_index] = {
            'category': category,
            'seen_items': set(),
            'scroll_position': 0,
            'last_item_count': 0,
            'stale_count': 0,
            'active': True
        }

    def quick_scrape_tab(self, driver, tab_index, scroll_count=3):
        """Quickly scrape a tab with limited scrolling"""
        if not self.tab_states[tab_index]['active']:
            return False
            
        try:
            driver.switch_to.window(driver.window_handles[tab_index])
            tab_state = self.tab_states[tab_index]
            category = tab_state['category']
            
            # Quick wait for content
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='explore-item']"))
            )
            
            new_videos_found = False
            explore_items = self.get_explore_items(driver)
            
            if not explore_items:
                tab_state['stale_count'] += 1
                if tab_state['stale_count'] >= 3:
                    tab_state['active'] = False
                    print(f"Tab {tab_index}: Deactivated {category['display']} - no content")
                return False

            # Process current items
            for item in explore_items:
                video_data = self.extract_video_data_for_tab_quick(item, category, tab_state['seen_items'])
                if video_data:
                    with self._lock:
                        self.all_video_info.append(video_data)
                    new_videos_found = True

            # Quick scroll multiple times
            current_item_count = len(explore_items)
            for _ in range(scroll_count):
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(0.5)  # Quick scroll
            
            # Check if we're getting new content
            if current_item_count == tab_state['last_item_count']:
                tab_state['stale_count'] += 1
                if tab_state['stale_count'] >= 5:
                    tab_state['active'] = False
                    print(f"Tab {tab_index}: Deactivated {category['display']} - reached end")
            else:
                tab_state['stale_count'] = 0
                tab_state['last_item_count'] = current_item_count
            
            return new_videos_found
            
        except Exception as e:
            print(f"Tab {tab_index}: Quick scrape error: {e}")
            return False

    def extract_video_data_for_tab_quick(self, item, category, tab_seen_items):
        """Quick video data extraction with minimal processing"""
        try:
            video_link = item.find("a", class_=lambda x: x and "css-1mdo0pl-AVideoContainer" in x)
            video_url = video_link['href'] if video_link else None

            if video_url and video_url not in tab_seen_items:
                tab_seen_items.add(video_url)
                with self._lock:
                    if video_url not in self.seen_items:
                        self.seen_items.add(video_url)
                        # Quick data extraction
                        img_tag = item.find("img")
                        likes_div = item.find("div", class_=lambda x: x and "css-qptaao-DivIconText" in x)
                        
                        video_data = {
                            "url": video_url,
                            "thumbnail": img_tag["src"] if img_tag else None,
                            "description": img_tag.get("alt", "") if img_tag else None,
                            "likes": likes_div.find("span").get_text(strip=True) if likes_div and likes_div.find("span") else None,
                            "category": category['slug']
                        }
                        return video_data
        except Exception:
            pass  # Skip problematic items quickly
        return None

    def scrape_videos_multi_tab_fast(self, max_categories=5, max_rounds=50, save_interval=10):
        """Fast multi-tab scraping with quick switching"""
        driver = self.setup_browser()
        try:
            # Get initial page to fetch categories
            driver.get("https://www.tiktok.com/explore")
            categories = self.get_categories(driver)
            
            if max_categories:
                categories = categories[:max_categories]
            
            print(f"Starting fast multi-tab scraping for {len(categories)} categories")
            
            # Open tabs and initialize states
            for i, category in enumerate(categories):
                self.open_category_tab(driver, category, i)
                self.init_tab_state(i, category)
                time.sleep(0.5)  # Quick delay
            
            # Round-robin tab switching
            round_count = 0
            videos_found_this_round = True
            
            while round_count < max_rounds and videos_found_this_round:
                videos_found_this_round = False
                active_tabs = [i for i, state in self.tab_states.items() if state['active']]
                
                if not active_tabs:
                    print("No active tabs remaining")
                    break
                
                print(f"Round {round_count + 1}: Processing {len(active_tabs)} active tabs")
                
                # Quick switch between tabs
                for tab_index in active_tabs:
                    category_name = self.tab_states[tab_index]['category']['display']
                    print(f"  Switching to tab {tab_index}: {category_name}")
                    
                    found_videos = self.quick_scrape_tab(driver, tab_index, scroll_count=2)
                    if found_videos:
                        videos_found_this_round = True
                    
                    time.sleep(0.2)  # Brief pause between tab switches
                
                round_count += 1
                
                # Periodic save
                if round_count % save_interval == 0:
                    with self._lock:
                        self.save_video_info()
                    print(f"Round {round_count}: Saved {len(self.all_video_info)} videos")
            
            # Final save
                self.save_video_info()
            print(f"Fast multi-tab scraping completed in {round_count} rounds")
            print(f"Total videos: {len(self.all_video_info)}")
            
        finally:
            driver.quit()

    def scrape_videos(self, output_callback=None):
        """Original single-tab scraping method (kept for backward compatibility)"""
        url = "https://www.tiktok.com/explore"
        driver = self.setup_browser()
        try:
            driver.get(url)

            categories = self.get_categories(driver)

            for category in categories:
                print(f"Switching to category: {category['display']}")
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(5)
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
                            video_data['category'] = category['slug']
                            self.all_video_info.append(video_data)
                            if output_callback:
                                output_callback(video_data)

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
    def scrape_videos_by_one_category(self, category: dict
                                      , output_callback=None, max_crawled_items = 2000):
        """Original single-tab scraping method (kept for backward compatibility)"""
        url = "https://www.tiktok.com/explore"
        driver = self.setup_browser()
        self.all_video_info = []
        try:
            driver.get(url)
            print(f"Switching to category: {category['display']}")
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(5)
            retry_count = 0
            max_retries = 2
            while retry_count < max_retries:
                try:
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
                        print(f"Error removing captcha container or modal overlays: {e}")
                    
                    category_button = driver.find_element(By.XPATH, f"//span[text()='{category['display']}']")
                    category_button.click()
                    break
                except Exception as e:
                    retry_count += 1
                    print(f"Retry {retry_count}/{max_retries} for category '{category['display']}': {e}")
                    try:
                        driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(2)
                        arrow_icon = driver.find_element(By.CLASS_NAME, "css-1wvr0tq-DivArrowContainer e13i6o2410")
                        arrow_icon.click()
                    except Exception as arrow_error:
                        print(f"Failed to click arrow icon: {arrow_error}")
                    time.sleep(2)
            else:
                print(f"Failed to select category '{category['display']}' after {max_retries} retries.")
            time.sleep(2)
            _max_crawlled_items = 0

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
                        video_data['category'] = category['category_slug']
                        self.all_video_info.append(video_data)
                        if output_callback:
                            output_callback(video_data)

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
                _max_crawlled_items += len(new_video_urls)
                if _max_crawlled_items >= max_crawled_items:
                    print(f"Reached max crawl limit of {_max_crawlled_items} items.")
                    break
        finally:
            driver.quit()

if __name__ == "__main__":
    scraper = TikTokVideoScraper()
    # Use fast multi-tab scraping (new optimized method)
    scraper.scrape_videos_multi_tab_fast(max_categories=5, max_rounds=30, save_interval=5)
    
    # Or use previous multi-tab method
    # scraper.scrape_videos_multi_tab(max_categories=5)
    
    # Or use original single-tab method
    # scraper.scrape_videos()
