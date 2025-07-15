import os
import undetected_chromedriver as uc

class RealBrowser:
    def __init__(self, profile_dir="./browser_profile"):
        self.driver = None
        # Store browser data in a persistent directory
        self.profile_dir = os.path.abspath(profile_dir)
        os.makedirs(self.profile_dir, exist_ok=True)

    def setup_browser(self):
        options = uc.ChromeOptions()
        # options.add_argument('--headless')
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
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        # Allow multiple tabs and improve performance
        options.add_argument('--max_old_space_size=4096')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        
        # Persist all browser data in self.profile_dir
        # options.add_argument(f'--user-data-dir={self.profile_dir}')

        self.driver = uc.Chrome(options=options)
        return self.driver

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

    def quit_browser(self):
        if self.driver:
            self.driver.quit()


# Example usage:
# if __name__ == "__main__":
#     browser = RealBrowser()
#     driver = browser.setup_browser()
#     driver.get("https://www.tiktok.com/explore")
#     browser.open_new_tab("https://www.google.com")
#     browser.quit_browser()