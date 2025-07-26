import re
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
from tiktokcomment import TiktokComment
from tiktokcomment.typing import Comments

def extract_aweme_id(url: str):
    # Try to extract aweme_id from TikTok video URL
    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)
    # If input is already an aweme_id
    if re.match(r"^\d+$", url):
        return url
    return None

def crawl_single_comment(aweme_id: str, output: str):
    logger.info(f'start scrap comments {aweme_id}')
    comments: Comments = TiktokComment()(aweme_id=aweme_id)
    if not os.path.exists(output):
        os.makedirs(output)
    final_path = os.path.join(output, f"{aweme_id}.json")
    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump(comments.dict, f, ensure_ascii=False)
    logger.info(f'save comments {aweme_id} on {final_path}')
    return final_path

def crawl_comments_multithreaded(video_urls, output='data/', max_workers=5):
    aweme_ids = []
    for url in video_urls:
        aweme_id = extract_aweme_id(url)
        if aweme_id:
            aweme_ids.append(aweme_id)
        else:
            logger.warning(f"Could not extract aweme_id from: {url}")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(crawl_single_comment, aweme_id, output) for aweme_id in aweme_ids]
        results = []
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                logger.error(f"Error crawling comments: {e}")
        return results

# Example usage:
video_urls = [
"https://www.tiktok.com/@quannguyenpuleofficial/video/7529740610798898448"
]
crawl_comments_multithreaded(video_urls, output='data/', max_workers=5)