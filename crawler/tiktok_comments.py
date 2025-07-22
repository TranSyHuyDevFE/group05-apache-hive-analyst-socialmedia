import pandas as pd
import re
import random

# === CONSTANTS ===
INPUT_FILE = "tiktok10.csv"
OUTPUT_FILE = "comments_cleaned2.csv"
VIDEO_URL = "https://www.tiktok.com/@kimanhne_36/video/7525671270936022290"

# === FUNCTIONS ===

def convert_likes(like):
    if pd.isna(like): return 0
    like = str(like).strip().upper()
    if 'K' in like:
        try:
            return int(float(like.replace('K', '')) * 1000)
        except:
            return 0
    try:
        return int(like)
    except:
        return 0

def random_date_in_may_to_july():
    day = random.randint(1, 28)
    month = random.randint(5, 7)
    return f"{day:02d}-{month:02d}-2025"

def extract_username(url):
    try:
        match = re.search(r"@[\w.]+", str(url))
        return match.group(0) if match else ""
    except:
        return ""

# === LOAD DATA ===
try:
    df = pd.read_csv(INPUT_FILE, encoding='utf-8', dtype=str)  # Bắt buộc ép string toàn bộ
except Exception as e:
    print(f"error ===>: {e}")
    exit()

# === format all to string ===
df = df.astype(str)

# === CLEANING ===
if 'username' in df.columns:
    df['username'] = df['username'].apply(extract_username)

if 'likes' in df.columns:
    df['likes'] = df['likes'].apply(convert_likes)

if 'timestamp' in df.columns:
    df['timestamp'] = df['timestamp'].apply(lambda x: random_date_in_may_to_july())


df['video_url'] = VIDEO_URL

columns = list(df.columns)

# === REORDER COLUMNS ===
ordered = []
for col in ['username', 'comment', 'timestamp', 'likes']:
    if col in columns:
        ordered.append(col)
if 'video_url' in columns:
    ordered.append('video_url')

for col in columns:
    if col not in ordered:
        ordered.append(col)

df = df[ordered]

# === genarate file scv ===
df.to_csv(OUTPUT_FILE, index=False)
print(f"one: {OUTPUT_FILE}")
