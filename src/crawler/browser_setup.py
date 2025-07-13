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
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-features=VizDisplayCompositor')
        # Persist all browser data in self.profile_dir
        options.add_argument(f'--user-data-dir={self.profile_dir}')

        self.driver = uc.Chrome(options=options)
        return self.driver

    def open_new_tab(self, url="about:blank"):
        if self.driver:
            self.driver.execute_script(f"window.open('{url}', '_blank');")

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