CREATE OR REPLACE VIEW v_top_hashtags AS
WITH cleaned_data AS (
  SELECT 
    video_url,
    regexp_replace(
      regexp_replace(hashtags, '^\\s*\\[|\\]\\s*$', ''), -- Remove outer brackets if present
      '["\'\\[\\]]', '' -- Remove any remaining quotes or brackets
    ) as clean_hashtags
  FROM tiktok_video_info_details
  WHERE hashtags IS NOT NULL AND hashtags != ''
)
SELECT 
  trim(hashtag) as clean_hashtag,
  COUNT(*) AS hashtag_count,
  COUNT(DISTINCT video_url) as video_count
FROM cleaned_data
LATERAL VIEW OUTER explode(split(clean_hashtags, ',')) t AS hashtag
WHERE trim(hashtag) != ''
GROUP BY trim(hashtag)
HAVING hashtag_count > 0
ORDER BY hashtag_count DESC

CREATE OR REPLACE VIEW v_trending_music AS
SELECT
  music_title AS track_name,
  COUNT(DISTINCT video_url) AS usage_count,
  COALESCE(SUM(CAST(likes AS BIGINT)), 0) AS total_likes,
  COALESCE(SUM(CAST(comments AS BIGINT)), 0) AS total_comments,
  COALESCE(SUM(CAST(shares AS BIGINT)), 0) AS total_shares,
  COALESCE(SUM(CAST(likes AS BIGINT)), 0) + COALESCE(SUM(CAST(comments AS BIGINT)), 0) + COALESCE(SUM(CAST(shares AS BIGINT)), 0) AS total_engagement
FROM tiktok_video_info_details
WHERE music_title IS NOT NULL AND music_title != ''
GROUP BY music_title
ORDER BY usage_count DESC;

CREATE OR REPLACE VIEW v_top_category_trending AS
SELECT
  v.category AS category_name,
  COUNT(DISTINCT v.url) AS video_count,
  COALESCE(SUM(CAST(d.likes AS BIGINT)), 0) AS total_likes,
  COALESCE(SUM(CAST(d.comments AS BIGINT)), 0) AS total_comments,
  COALESCE(SUM(CAST(d.shares AS BIGINT)), 0) AS total_shares,
  COALESCE(SUM(CAST(d.likes AS BIGINT)), 0) + COALESCE(SUM(CAST(d.comments AS BIGINT)), 0) + COALESCE(SUM(CAST(d.shares AS BIGINT)), 0) AS total_engagement
FROM tiktok_video_info v
LEFT JOIN tiktok_video_info_details d
  ON v.url = d.video_url
WHERE v.category IS NOT NULL AND v.category != ''
GROUP BY v.category
ORDER BY video_count DESC;

CREATE OR REPLACE VIEW v_trending_videos AS
SELECT
  video_url,
  username,
  nickname,
  description,
  music_title AS music,
  COALESCE(CAST(likes AS INT), 0) AS likes,
  COALESCE(CAST(comments AS INT), 0) AS comments,
  COALESCE(CAST(shares AS INT), 0) AS shares,
  (COALESCE(CAST(likes AS INT), 0) + COALESCE(CAST(comments AS INT), 0) + COALESCE(CAST(shares AS INT), 0)) AS total_engagement
FROM tiktok_video_info_details
ORDER BY total_engagement DESC;

-- ===== SENTIMENT ANALYSIS VIEWS FOR DASHBOARD =====
-- View for trending videos and sentiment analysis by crawl date
CREATE OR REPLACE VIEW v_daily_trending_analysis AS
WITH daily_videos AS (
  SELECT 
    v.crawl_date,
    v.video_url,
    v.username,
    v.nickname,
    v.description,
    v.music_title,
    COALESCE(CAST(v.likes AS INT), 0) AS video_likes,
    COALESCE(CAST(v.comments AS INT), 0) AS video_comments,
    COALESCE(CAST(v.shares AS INT), 0) AS video_shares,
    (COALESCE(CAST(v.likes AS INT), 0) + 
     COALESCE(CAST(v.comments AS INT), 0) + 
     COALESCE(CAST(v.shares AS INT), 0)) AS total_engagement,
    v.time_published,
    ROW_NUMBER() OVER (PARTITION BY v.crawl_date ORDER BY (COALESCE(CAST(v.likes AS INT), 0) + COALESCE(CAST(v.comments AS INT), 0) + COALESCE(CAST(v.shares AS INT), 0)) DESC) as rank_by_date
  FROM tiktok_video_info_details v
  WHERE v.video_url IS NOT NULL AND v.crawl_date IS NOT NULL
)
SELECT 
  dv.crawl_date,
  dv.video_url,
  dv.username,
  dv.nickname,
  SUBSTR(dv.description, 1, 100) AS short_description,
  dv.music_title,
  dv.video_likes,
  dv.video_comments,
  dv.video_shares,
  dv.total_engagement,
  dv.rank_by_date,
  -- Comment sentiment analysis
  COUNT(c.content) AS total_comments,
  SUM(CASE WHEN c.sentiment = 'POS' THEN 1 ELSE 0 END) AS positive_comments,
  SUM(CASE WHEN c.sentiment = 'NEG' THEN 1 ELSE 0 END) AS negative_comments,
  SUM(CASE WHEN c.sentiment = 'NEU' THEN 1 ELSE 0 END) AS neutral_comments,
  -- Sentiment percentages
  ROUND((SUM(CASE WHEN c.sentiment = 'POS' THEN 1 ELSE 0 END) * 100.0 / 
    NULLIF(COUNT(c.content), 0)), 2) AS positive_pct,
  ROUND((SUM(CASE WHEN c.sentiment = 'NEG' THEN 1 ELSE 0 END) * 100.0 / 
    NULLIF(COUNT(c.content), 0)), 2) AS negative_pct,
  ROUND((SUM(CASE WHEN c.sentiment = 'NEU' THEN 1 ELSE 0 END) * 100.0 / 
    NULLIF(COUNT(c.content), 0)), 2) AS neutral_pct,
  -- Engagement metrics
  SUM(COALESCE(c.likes, 0)) AS total_comment_likes,
  AVG(COALESCE(c.likes, 0)) AS avg_comment_likes,
  -- Sentiment score
  (SUM(CASE WHEN c.sentiment = 'POS' THEN 1 ELSE 0 END) - 
   SUM(CASE WHEN c.sentiment = 'NEG' THEN 1 ELSE 0 END)) AS sentiment_score
FROM daily_videos dv
LEFT JOIN tiktok_comments c ON dv.video_url = c.video_url
WHERE dv.rank_by_date <= 10  -- Top 10 videos per day
GROUP BY 
  dv.crawl_date,
  dv.video_url,
  dv.username,
  dv.nickname,
  dv.description,
  dv.music_title,
  dv.video_likes,
  dv.video_comments,
  dv.video_shares,
  dv.total_engagement,
  dv.rank_by_date
ORDER BY 
  dv.crawl_date DESC,
  dv.rank_by_date;