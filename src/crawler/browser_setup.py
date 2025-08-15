import os
import json
import pickle
import logging
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_path = os.getenv("CHROME_BINARY_PATH", "/usr/bin/google-chrome-stable")
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealBrowser:
    def __init__(self, profile_dir="./browser_profile"):
        self.driver = None
        # Store browser data in a persistent directory
        self.profile_dir = os.path.abspath(profile_dir)
        self.cookies_file = os.path.join(self.profile_dir, "cookies.pkl")
        self.session_file = os.path.join(self.profile_dir, "session_info.json")
        os.makedirs(self.profile_dir, exist_ok=True)
        logger.info(f"Browser profile directory: {self.profile_dir}")

    def setup_browser(self, load_previous_session=True):
        """Setup browser with enhanced persistence options"""
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-features=VizDisplayCompositor')

        # Enable multiple tabs and windows
        options.add_argument('--enable-features=VizDisplayCompositor')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Allow multiple tabs and improve performance
        # options.add_argument('--max_old_space_size=4096')
        options.add_argument('--disable-background-timer-throttling')
        # options.add_argument('--disable-backgrounding-occluded-windows')
        # options.add_argument('--disable-renderer-backgrounding')

        # Enhanced persistence settings
        options.add_argument(f'--user-data-dir={self.profile_dir}')
        options.add_argument('--profile-directory=Default')
        # options.add_argument('--restore-last-session')
        # options.add_argument('--disable-session-crashed-bubble')
        options.add_argument('--disable-infobars')

        # Cookie and cache persistence
        # options.add_argument('--aggressive-cache-discard')
        # options.add_argument('--enable-aggressive-domstorage-flushing')

        try:
            self.driver = uc.Chrome(options=options)
            logger.info("Browser started successfully")

            # Load previous session if requested
            if load_previous_session:
                self.load_session_info()

            return self.driver
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise

    def open_new_tab(self, url="about:blank"):
        """Open a new tab and optionally navigate to a URL"""
        if self.driver:
            self.driver.execute_script(f"window.open('{url}', '_blank');")
            # Switch to the new tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            return self.driver.current_window_handle

    def switch_to_tab(self, tab_handle):
        """Switch to a specific tab by handle"""
        if self.driver and tab_handle in self.driver.window_handles:
            self.driver.switch_to.window(tab_handle)
            return True
        return False

    def close_current_tab(self):
        """Close the current tab"""
        if self.driver and len(self.driver.window_handles) > 1:
            self.driver.close()
            # Switch to the first available tab
            self.driver.switch_to.window(self.driver.window_handles[0])

    def get_all_tab_handles(self):
        """Get all tab handles"""
        if self.driver:
            return self.driver.window_handles
        return []

    def save_cookies(self, domain=None):
        """Save cookies to a file for persistence"""
        if not self.driver:
            logger.warning("No driver available to save cookies")
            return False

        try:
            cookies = self.driver.get_cookies()
            if domain:
                # Filter cookies by domain
                cookies = [
                    cookie for cookie in cookies if domain in cookie.get('domain', '')]

            with open(self.cookies_file, 'wb') as f:
                pickle.dump(cookies, f)
            logger.info(f"Saved {len(cookies)} cookies to {self.cookies_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
            return False

    def load_cookies(self, url=None):
        """Load cookies from file"""
        if not self.driver:
            logger.warning("No driver available to load cookies")
            return False

        if not os.path.exists(self.cookies_file):
            logger.info("No cookie file found")
            return False

        try:
            with open(self.cookies_file, 'rb') as f:
                cookies = pickle.load(f)

            # Navigate to a page first if URL provided
            if url:
                self.driver.get(url)

            # Add each cookie
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    logger.warning(
                        f"Failed to add cookie {cookie.get('name', 'unknown')}: {e}")

            logger.info(f"Loaded {len(cookies)} cookies")
            return True
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
            return False

    def save_session_info(self):
        """Save current session information"""
        if not self.driver:
            logger.warning("No driver available to save session info")
            return False

        try:
            session_info = {
                'current_url': self.driver.current_url,
                'window_handles': self.driver.window_handles,
                'current_window': self.driver.current_window_handle,
                'timestamp': datetime.now().isoformat(),
                'tab_urls': []
            }

            # Save URLs of all open tabs
            current_handle = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                try:
                    self.driver.switch_to.window(handle)
                    session_info['tab_urls'].append({
                        'handle': handle,
                        'url': self.driver.current_url,
                        'title': self.driver.title
                    })
                except Exception as e:
                    logger.warning(f"Failed to get info for tab {handle}: {e}")

            # Switch back to original tab
            self.driver.switch_to.window(current_handle)

            with open(self.session_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            logger.info(f"Session info saved to {self.session_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save session info: {e}")
            return False

    def load_session_info(self):
        """Load and restore previous session information"""
        if not os.path.exists(self.session_file):
            logger.info("No session file found")
            return False

        try:
            with open(self.session_file, 'r') as f:
                session_info = json.load(f)

            logger.info(
                f"Found session from {session_info.get('timestamp', 'unknown time')}")

            # Restore tabs if there were multiple
            tab_urls = session_info.get('tab_urls', [])
            if len(tab_urls) > 1:
                for i, tab_info in enumerate(tab_urls):
                    if i == 0:
                        # Navigate first tab
                        self.driver.get(tab_info['url'])
                    else:
                        # Open new tabs
                        self.open_new_tab(tab_info['url'])

            elif len(tab_urls) == 1:
                self.driver.get(tab_urls[0]['url'])

            return True
        except Exception as e:
            logger.error(f"Failed to load session info: {e}")
            return False

    def navigate_and_save_cookies(self, url, save_cookies_after=True):
        """Navigate to URL and optionally save cookies afterward"""
        if not self.driver:
            logger.warning("No driver available")
            return False

        try:
            # Load existing cookies first
            self.load_cookies(url)

            # Navigate to the URL
            self.driver.get(url)
            logger.info(f"Navigated to {url}")

            # Save cookies after navigation if requested
            if save_cookies_after:
                self.save_cookies()

            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            return False

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        if not self.driver:
            return None

        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except Exception as e:
            logger.warning(f"Element not found: {by}={value}, error: {e}")
            return None

    def quit_browser(self, save_session=True):
        """Quit browser with optional session saving"""
        if self.driver:
            try:
                if save_session:
                    self.save_cookies()
                    self.save_session_info()
                self.driver.quit()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error while closing browser: {e}")
        self.driver = None


# Example usage:
if __name__ == "__main__":
    # Create browser instance with persistent profile
    browser = RealBrowser(profile_dir="./browser_profile")

    try:
        # Setup browser (will load previous session if available)
        driver = browser.setup_browser(load_previous_session=True)

        # Navigate to a site and load/save cookies
        browser.navigate_and_save_cookies("https://www.tiktok.com/explore")

        # Open multiple tabs
        tab1 = browser.open_new_tab("https://www.google.com")
        tab2 = browser.open_new_tab("https://www.youtube.com")

        # Wait for some element (example)
        # search_box = browser.wait_for_element(By.NAME, "q")

        # Save current session state
        browser.save_session_info()
        browser.save_cookies()

        print(f"Browser profile stored in: {browser.profile_dir}")
        print(f"Cookies saved to: {browser.cookies_file}")
        print(f"Session info saved to: {browser.session_file}")

    finally:
        # Quit browser (automatically saves session and cookies)
        browser.quit_browser(save_session=True)
