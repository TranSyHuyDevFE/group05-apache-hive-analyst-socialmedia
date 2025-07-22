from playwright.sync_api import sync_playwright
import csv
import re
profile_path = "C:/Users/syhuy/AppData/Local/Google/Chrome/User Data"

def clean_text(text):
    return re.sub(r'[^\w\s,.!?@]', '', text).strip()

def crawl_comments(video_url: str, output_csv='comments.csv'):
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            headless=False,
            args=["--start-maximized"]
        )

        page = context.new_page()
        print(f"oppening ====>>>>>> : {video_url}")
        page.goto(video_url)
        page.wait_for_timeout(5000)

        for _ in range(10):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1200)

        # Ready to query comments DOM 
        comment_items = page.query_selector_all("div.css-1gstnae-DivCommentItemWrapper")
        comments = []

        for item in comment_items:
            try:
                username = item.query_selector("div[data-e2e^='comment-username'] p").inner_text() or ""
                comment_text = item.query_selector("span[data-e2e^='comment-level'] p").inner_text() or ""
                likes = item.query_selector("div[aria-label*='Like video'] span")
                likes = likes.inner_text() if likes else "0"
                timestamp = item.query_selector("div.css-1lglotn-DivCommentSubContentWrapper span")
                timestamp = timestamp.inner_text() if timestamp else ""

                comments.append({
                    "username": clean_text(username),
                    "comment": clean_text(comment_text),
                    "likes": int(re.sub(r"\D", "", likes) or "0"),
                    "timestamp": timestamp.strip()
                })
            except Exception as e:
                print(f"[!] error: {e}")
                continue
            
        # Export to CSV
        with open(output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "comment", "likes", "timestamp"])
            writer.writeheader()
            writer.writerows(comments)

        print(f" ===> {len(comments)} comments {output_csv}")
        context.close()

# input here the TikTok video URL    
crawl_comments("https://www.tiktok.com/@8kgocnhin/video/7528732251836878088")
