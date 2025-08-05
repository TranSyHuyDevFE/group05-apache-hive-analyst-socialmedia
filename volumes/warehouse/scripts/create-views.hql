CREATE OR REPLACE VIEW v_top_hashtags AS
SELECT trim(regexp_replace(hashtag, '[\\[\\]\'\"\\s]', '')) as clean_hashtag, COUNT(*) AS count
FROM tiktok_video_info_details
LATERAL VIEW explode(split(hashtags, ',')) t AS hashtag
WHERE hashtag != '' AND hashtag IS NOT NULL
GROUP BY trim(regexp_replace(hashtag, '[\\[\\]\'\"\\s]', ''));

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